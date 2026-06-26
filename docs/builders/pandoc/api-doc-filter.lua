-- api-doc-filter.lua
-- Pandoc Lua filter for Python API documentation
--
-- Transforms:
--   1. <div class="namespace-rule" id="fqn">  → thick rule + hyperref anchor (LaTeX)
--                                              → styled <hr id="fqn">         (HTML)
--   2. <div class="member-rule">               → thin rule                    (LaTeX/HTML)
--   3. <div class="member-name">               → bold teal monospace block    (LaTeX)
--                                              → styled div                   (HTML, passthrough)
--   4. <a id="fqn"></a>                        → \phantomsection\hypertarget  (LaTeX)
--                                              → passthrough                  (HTML)
--   5. <small>...</small>                      → gray footnotesize mono       (LaTeX)
--   6. Table (pipe or grid)                    → styled longtable             (LaTeX)
--   7. Header with auto-generated id           → \phantomsection anchor       (LaTeX)
--
-- Usage:
--   pandoc input.md -o output.pdf \
--     --lua-filter=api-doc-filter.lua \
--     --template=api-doc-template.latex \
--     --pdf-engine=xelatex \
--     --from markdown+raw_html

-- ─── Utilities ────────────────────────────────────────────────────────────────

local function is_latex()
  return FORMAT == "latex" or FORMAT == "pdf"
end

local function is_html()
  return FORMAT == "html" or FORMAT == "html5" or FORMAT == "html4"
end

local function latex_inline(s)  return pandoc.RawInline("latex", s)  end
local function latex_block(s)   return pandoc.RawBlock("latex", s)   end
local function html_block(s)    return pandoc.RawBlock("html", s)    end

-- Escape special LaTeX characters in plain text strings
local function latex_escape(s)
  s = s:gsub("\\", "\\textbackslash{}")
  s = s:gsub("{",  "\\{")
  s = s:gsub("}",  "\\}")
  s = s:gsub("#",  "\\#")
  s = s:gsub("%$", "\\$")
  s = s:gsub("%%", "\\%%")
  s = s:gsub("&",  "\\&")
  s = s:gsub("_",  "\\_")
  s = s:gsub("%^", "\\^{}")
  s = s:gsub("~",  "\\textasciitilde{}")
  return s
end

-- Render a Pandoc Inlines list to a LaTeX string (best-effort for table cells)
local function inlines_to_latex(inlines)
  local parts = {}
  for _, el in ipairs(inlines) do
    if el.t == "Str" then
      parts[#parts + 1] = latex_escape(el.text)
    elseif el.t == "Space" or el.t == "SoftBreak" then
      parts[#parts + 1] = " "
    elseif el.t == "LineBreak" then
      parts[#parts + 1] = "\\\\"
    elseif el.t == "Code" then
      parts[#parts + 1] = "\\texttt{" .. latex_escape(el.text) .. "}"
    elseif el.t == "Strong" then
      parts[#parts + 1] = "\\textbf{" .. inlines_to_latex(el.content) .. "}"
    elseif el.t == "Emph" then
      parts[#parts + 1] = "\\textit{" .. inlines_to_latex(el.content) .. "}"
    elseif el.t == "Link" then
      local label = inlines_to_latex(el.content)
      local target = el.target
      if target:match("^#") then
        -- Internal link: use hyperref \hyperlink
        local anchor = target:sub(2)  -- strip leading #
        parts[#parts + 1] = "\\hyperlink{" .. anchor .. "}{" .. label .. "}"
      else
        parts[#parts + 1] = "\\href{" .. target .. "}{" .. label .. "}"
      end
    elseif el.t == "RawInline" and el.format == "html" then
      -- Handle <code> tags inside table cells
      if el.text:match("^<code") then
        parts[#parts + 1] = "\\texttt{"
      elseif el.text == "</code>" then
        parts[#parts + 1] = "}"
      elseif el.text:match("^<a ") then
        local href = el.text:match('href=["\']([^"\']*)["\']')
        if href and href:match("^#") then
          local anchor = href:sub(2)
          parts[#parts + 1] = "\\hyperlink{" .. anchor .. "}{"
        else
          parts[#parts + 1] = "\\href{" .. (href or "") .. "}{"
        end
      elseif el.text == "</a>" then
        parts[#parts + 1] = "}"
      end
      -- other raw HTML tags: skip
    end
  end
  return table.concat(parts)
end

-- Render a Pandoc Blocks list to a LaTeX string (for multi-line table cells)
local function blocks_to_latex(blocks)
  local parts = {}
  for _, bl in ipairs(blocks) do
    if bl.t == "Plain" or bl.t == "Para" then
      parts[#parts + 1] = inlines_to_latex(bl.content)
    elseif bl.t == "CodeBlock" then
      parts[#parts + 1] = "\\texttt{" .. latex_escape(bl.text) .. "}"
    end
  end
  return table.concat(parts, " ")
end

-- ─── 1 & 2. Div class handlers (namespace-rule, member-rule, member-name) ────

function Div(el)
  local classes = el.classes or pandoc.List()

  -- ── namespace-rule ──────────────────────────────────────────────────────
  if classes:find("namespace-rule") then
    local ns_id = el.identifier
    if is_latex() then
      local anchor = ""
      if ns_id and ns_id ~= "" then
        local label = ns_id:gsub("[%.%-]", ":")
        anchor = string.format(
          "\\phantomsection\\label{%s}\\hypertarget{%s}{}",
          label, ns_id
        )
      end
      return latex_block(
        "\n\\vspace{10pt}\n" ..
        anchor .. "\n" ..
        "{\\color{ApiRuleHeavy}\\rule{\\linewidth}{2.5pt}}\n" ..
        "\\vspace{2pt}\n"
      )
    elseif is_html() then
      local id_attr = (ns_id and ns_id ~= "") and (' id="' .. ns_id .. '"') or ""
      return html_block(
        '<hr' .. id_attr ..
        ' class="namespace-rule"' ..
        ' style="border:none;border-top:3px solid #1a5276;margin:2rem 0 0.5rem 0;" />'
      )
    end
  end

  -- ── member-rule ─────────────────────────────────────────────────────────
  if classes:find("member-rule") then
    if is_latex() then
      return latex_block(
        "\n\\vspace{4pt}\n" ..
        "{\\color{ApiRuleLight}\\rule{\\linewidth}{0.6pt}}\n" ..
        "\\vspace{4pt}\n"
      )
    elseif is_html() then
      return html_block(
        '<hr class="member-rule"' ..
        ' style="border:none;border-top:1px solid #aab7b8;margin:1.5rem 0;" />'
      )
    end
  end

  -- ── heading-style divs (.h1-style … .h5-style) ─────────────────────────
  -- Renders with the same visual style as the matching heading level but
  -- emits no \section command, so it never appears in the TOC.
  -- Usage: <div class="h2-style">Section Title</div>
  local heading_styles = {
    ["h1-style"] = "\\color{ApiBlue}\\fontsize{20}{24}\\selectfont\\sffamily\\bfseries",
    ["h2-style"] = "\\color{ApiGray}\\fontsize{12}{15}\\selectfont\\sffamily\\bfseries",
    ["h3-style"] = "\\color{ApiBlue}\\fontsize{13}{16}\\selectfont\\sffamily\\bfseries",
    ["h4-style"] = "\\color{ApiTeal}\\fontsize{11}{14}\\selectfont\\ttfamily\\bfseries",
    ["h5-style"] = "\\color{ApiGray}\\fontsize{10}{13}\\selectfont\\sffamily\\itshape",
  }
  for cls, fmt in pairs(heading_styles) do
    if classes:find(cls) then
      if is_latex() then
        local text = latex_escape(pandoc.utils.stringify(el))
        if cls == "h2-style" then text = text:upper() end
        return latex_block(
          "\n\\vspace{6pt}\n" ..
          "{" .. fmt .. " " .. text .. "}\n" ..
          "\\vspace{2pt}\n"
        )
      end
      -- HTML: let Pandoc render the div; CSS handles presentation
      return nil
    end
  end

  -- ── pagebreak ────────────────────────────────────────────────────────────
  -- Explicit page break.  Usage: <div class="pagebreak"></div>
  if classes:find("pagebreak") then
    if is_latex() then
      return latex_block("\\newpage")
    elseif is_html() then
      return html_block('<div class="pagebreak"></div>')
    end
  end

  -- ── pagegroup ────────────────────────────────────────────────────────────
  -- Wraps a logical group of content that should not be orphaned mid-page.
  -- If less than 4 lines of space remain on the current page, LaTeX breaks
  -- to a new page before this group starts.  The group itself may still span
  -- multiple pages.  Nesting works: each inner pagegroup gets its own check.
  -- Usage: <div class="pagegroup">...</div>
  if classes:find("pagegroup") then
    if is_latex() then
      local result = pandoc.List()
      -- Require 8 lines of space before starting the group; if less is
      -- available LaTeX breaks to a new page first.
      result:insert(latex_block("\\needspace{8\\baselineskip}"))
      for i, b in ipairs(el.content) do
        result:insert(b)
        -- Glue the first block (label / heading) to the second block (table /
        -- code) so TeX cannot orphan the label at the bottom of a page.
        -- Penalty 9000 is overrideable in extremis (avoids overfull pages).
        if i == 1 and #el.content > 1 then
          result:insert(latex_block("\\nopagebreak[3]"))
        end
      end
      return result
    end
    -- HTML: passthrough as a plain div; CSS handles print behaviour
    return nil
  end

  -- ── member-name ─────────────────────────────────────────────────────────
  -- Contains the member name (attribute, function, method) as a styled block.
  -- In HTML this is a passthrough <div class="member-name"> styled by CSS.
  -- In LaTeX we emit a styled paragraph that mimics a heading visually
  -- without registering in the TOC or Pandoc heading hierarchy.
  if classes:find("member-name") then
    if is_latex() then
      -- Extract the text content for rendering
      local text = pandoc.utils.stringify(el)
      -- Look for an id on the div to use as a hyperref anchor
      local anchor_id = el.identifier
      local anchor = ""
      if anchor_id and anchor_id ~= "" then
        anchor = string.format(
          "\\phantomsection\\hypertarget{%s}{}",
          anchor_id
        )
      end
      return latex_block(
        anchor .. "\n" ..
        "\\vspace{4pt}\n" ..
        "{\\color{ApiTeal}\\ttfamily\\bfseries\\large " ..
        latex_escape(text) ..
        "}\n" ..
        "\\vspace{2pt}\n"
      )
    end
    -- HTML: let Pandoc render the div content as-is; CSS handles presentation
  end

  return nil
end

-- ─── 4. <a id="fqn"></a> anchor handling ─────────────────────────────────────
--
-- Pandoc parses <a id="..."></a> as two RawInline html nodes inside a Para.
-- We walk Inlines to catch the opening tag and emit a hypertarget in LaTeX.
-- In HTML we leave them untouched (native browser anchors).

function Inlines(inlines)
  if not is_latex() then return nil end

  local result = pandoc.List()
  local changed = false
  local i = 1

  while i <= #inlines do
    local el = inlines[i]

    if el.t == "RawInline" and el.format == "html" then
      -- ── <a id="..."> anchor ─────────────────────────────────────────────
      local anchor_id = el.text:match('^<a%s+id=["\']([^"\']+)["\']')
      if anchor_id then
        -- Emit \phantomsection\hypertarget; skip the matching </a>
        result:insert(latex_inline(
          string.format("\\phantomsection\\hypertarget{%s}{}", anchor_id)
        ))
        changed = true
        i = i + 1
        -- Skip the closing </a> if it immediately follows
        if i <= #inlines then
          local next = inlines[i]
          if next.t == "RawInline" and next.format == "html"
             and next.text:match("^</a>") then
            i = i + 1
          end
        end

      -- ── <small> open tag ────────────────────────────────────────────────
      elseif el.text:match("^<small") then
        result:insert(latex_inline("{\\color{ApiGray}\\footnotesize\\ttfamily "))
        changed = true
        i = i + 1

      -- ── </small> close tag ──────────────────────────────────────────────
      elseif el.text:match("^</small>") then
        result:insert(latex_inline("}"))
        changed = true
        i = i + 1

      -- ── <code> / </code> inline tags (inside member-name divs, etc.) ───
      elseif el.text:match("^<code") then
        result:insert(latex_inline("\\texttt{"))
        changed = true
        i = i + 1

      elseif el.text == "</code>" then
        result:insert(latex_inline("}"))
        changed = true
        i = i + 1

      else
        result:insert(el)
        i = i + 1
      end
    else
      result:insert(el)
      i = i + 1
    end
  end

  return changed and result or nil
end

-- Span handler: [text]{.classname}
-- Supports .small and .qualified-name for gray monospace inline text.
function Span(el)
  if not is_latex() then return nil end
  local classes = el.classes or pandoc.List()
  if classes:find("small") or classes:find("qualified-name") then
    local inner = inlines_to_latex(el.content)
    return pandoc.Inlines({
      latex_inline("{\\color{ApiGray}\\footnotesize\\ttfamily " .. inner .. "}")
    })
  end
  return nil
end

-- ─── 6. HorizontalRule (---) ─────────────────────────────────────────────────
--
-- Pandoc emits \begin{center}\rule{0.5\linewidth}{0.5pt}\end{center} by default,
-- giving a short centered rule. We intercept here to produce a full-width grey
-- rule that is left-justified, matching \memberRule in the template.

function HorizontalRule()
  if is_latex() then
    return latex_block(
      "\n\\vspace{4pt}\n" ..
      "{\\color{ApiRuleLight}\\rule{\\linewidth}{0.6pt}}\n" ..
      "\\vspace{4pt}\n"
    )
  end
  -- HTML: return nil and let CSS handle the native <hr>
  return nil
end

-- ─── 8. Table → styled longtable (LaTeX) ─────────────────────────────────────
--
-- Pandoc parses both pipe tables and grid tables to the same native Table AST.
-- This handler emits a styled longtable for LaTeX output; HTML output is
-- left to Pandoc's default HTML table writer (which is already correct).

function Table(el)
  if not is_latex() then return nil end

  -- Pandoc 3.x uses el.colspecs (plural); each entry is {AlignX, ColWidthX}
  -- ColWidthDefault is nil in Lua; a fractional width is a number 0–1.
  local colspecs = el.colspecs or {}
  local ncols = #colspecs

  if ncols == 0 then return nil end  -- safety: let Pandoc handle degenerate tables

  local col_specs = {}
  for i, cs in ipairs(colspecs) do
    local w = cs[2]  -- number (fraction) or nil (ColWidthDefault)
    if type(w) == "number" and w > 0 then
      col_specs[i] = string.format("p{%.4f\\linewidth}", w * 0.97)
    else
      col_specs[i] = "l"
    end
  end
  local col_str = table.concat(col_specs, " ")

  local lines = {}

  lines[#lines+1] = "\\begin{longtable}{" .. col_str .. "}"
  lines[#lines+1] = "\\rowcolor{TableHead}"

  -- Header row
  local head = el.head
  if head and head.rows and #head.rows > 0 then
    local row = head.rows[1]
    local cells = {}
    for _, cell in ipairs(row.cells) do
      local text = blocks_to_latex(cell.contents)
      cells[#cells+1] = "\\color{white}\\sffamily\\bfseries\\small " .. text
    end
    lines[#lines+1] = table.concat(cells, " & ") .. " \\\\"
    lines[#lines+1] = "\\hline"
    lines[#lines+1] = "\\endfirsthead"
    -- Continuation header
    lines[#lines+1] = "\\rowcolor{TableHead}"
    lines[#lines+1] = table.concat(cells, " & ") .. " \\\\"
    lines[#lines+1] = "\\hline"
    lines[#lines+1] = "\\endhead"
  end

  -- Body rows
  local body = el.bodies and el.bodies[1]
  if body then
    for r, row in ipairs(body.body) do
      -- Alternating row colour
      if r % 2 == 0 then
        lines[#lines+1] = "\\rowcolor{TableEven}"
      else
        lines[#lines+1] = "\\rowcolor{TableOdd}"
      end
      local cells = {}
      for _, cell in ipairs(row.cells) do
        cells[#cells+1] = "\\small " .. blocks_to_latex(cell.contents)
      end
      lines[#lines+1] = table.concat(cells, " & ") .. " \\\\"
    end
  end

  lines[#lines+1] = "\\hline"
  lines[#lines+1] = "\\end{longtable}"

  return latex_block(table.concat(lines, "\n"))
end

-- ─── 9. Header \phantomsection for namespace headings ────────────────────────
--
-- Namespace headings (H1, H2) are still Markdown headings.
-- Pandoc emits them fine, but hyperref can mis-target links to headings
-- that appear after a float or other non-text element.
-- We inject \phantomsection to keep links accurate.

function Header(el)
  if not is_latex() then return nil end
  if el.level > 2 then return nil end   -- only namespace-level headings

  local id = el.identifier
  if id and id ~= "" then
    local anchor = latex_block(
      string.format("\\phantomsection\\hypertarget{%s}{}", id)
    )
    return pandoc.Blocks({ anchor, el })
  end
  return nil
end

-- ─── 10. Docstring section labels (bold-only paragraphs) ────────────────────
--
-- Paragraphs that consist entirely of a single Strong element are docstring
-- section labels: Declaration, Parameters, Returns, Raises, Yields, See Also…
-- A small lead-in space is added before them to visually separate the
-- description text above from the technical sections below.

function Para(el)
  if not is_latex() then return nil end
  if #el.content == 1 and el.content[1].t == "Strong" then
    return pandoc.Blocks({
      latex_block("\\vspace{6pt}"),
      el,
    })
  end
  return nil
end

-- ─── 11. Code block language normalisation ───────────────────────────────────

function CodeBlock(el)
  local classes = el.classes or pandoc.List()
  if classes:find("python-declaration") then
    el.classes = pandoc.List({"python"})
    return el
  end
  return nil
end
