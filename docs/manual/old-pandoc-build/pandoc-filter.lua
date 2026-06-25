-- function Div(el)
--   -- el.classes is a list of classes on this Div
--   for _, c in ipairs(el.classes) do
--     if c == "only-web" then
--       return {}  -- delete the div and its content
--     end
--   end
-- end

-- Relavant JSON: { "t": "RawBlock", "c": [ "html", "<!-- pagebreak -->" ] },
function RawBlock(el)
  -- Must use string.find(text, "", 1, true) or the "-" characters mess things up?
  if el.format == 'html' and string.find(el.text, "<!-- pagebreak -->", 1, true) then
    return pandoc.RawBlock("latex", "\\newpage")
  end
end

function dump(t, indent)
  indent = indent or 0
  for k, v in pairs(t) do
    local formatting = string.rep("  ", indent) .. k .. ": "
    if type(v) == "table" then
      print(formatting)
      dump(v, indent + 1)
    else
      print(formatting .. tostring(v))
    end
  end
end

-- Admonition definitions
function Div(el)
  if el.classes:includes("note") then
    el.content:insert(1, pandoc.Para({ pandoc.Str("Note:") }))
    return {
      pandoc.RawBlock("latex", "\\begin{note-box}"),
      el,
      pandoc.RawBlock("latex", "\\end{note-box}")
    }
  end
  if el.classes:includes("tip") then
    el.content:insert(1, pandoc.Para({ pandoc.Str("Tip:") }))
    return {
      pandoc.RawBlock("latex", "\\begin{tip-box}"),
      el,
      pandoc.RawBlock("latex", "\\end{tip-box}")
    }
  end
  if el.classes:includes("info") then
    el.content:insert(1, pandoc.Para({ pandoc.Str("Info:") }))
    return {
      pandoc.RawBlock("latex", "\\begin{info-box}"),
      el,
      pandoc.RawBlock("latex", "\\end{info-box}")
    }
  end
  if el.classes:includes("warning") then
    el.content:insert(1, pandoc.Para({ pandoc.Str("Warning:") }))
    return {
      pandoc.RawBlock("latex", "\\begin{warning-box}"),
      el,
      pandoc.RawBlock("latex", "\\end{warning-box}")
    }
  end
  if el.classes:includes("danger") then
    el.content:insert(1, pandoc.Para({ pandoc.Str("Danger:") }))
    return {
      pandoc.RawBlock("latex", "\\begin{danger-box}"),
      el,
      pandoc.RawBlock("latex", "\\end{danger-box}")
    }
  end

  if el.classes:includes("hrule") then
    if FORMAT:match("latex") or FORMAT:match("pdf") then
      return pandoc.RawBlock("latex", "\\noindent\\rule{0.5\\textwidth}{0.4pt}")
    else
      return pandoc.RawBlock("html", "<hr style='width:50%; margin-left:0;'>")
    end
  end

  if el.classes:includes("lefttable") then
    if FORMAT:match("latex") or FORMAT:match("pdf") then
      return {
        pandoc.RawBlock("latex", "\\begingroup\\raggedright"),
        pandoc.Div(el.content),
        pandoc.RawBlock("latex", "\\endgroup")
      }
    else
      el.attributes["style"] = "text-align: left; margin-right: auto;"
      return el
    end
  end
end

function Span(el)
  if el.classes:includes("largetext") then
    if FORMAT:match("latex") or FORMAT:match("pdf") then
      return {
        pandoc.RawInline("latex", "\\LARGE "),
        pandoc.Span(el.content),
        pandoc.RawInline("latex", "\\normalsize ")
      }
    else
      -- In HTML/markdown readers, just return the span as-is (unstyled)
      return el
    end
  end
end

-- function Image(el)
--   print("--- IMAGE DUMP")
--   dump(el)
--   print("--- IMAGE ATTR DUMP")
--   dump(el.attr)
--   -- el.attr.attributes["placement"] = "H"
--   -- el.attr.attributes["width"] = "100%"
--   dump(el.attr.attributes)
--   print("--- IMAGE ATTR DUMP (AFTER)")
--   dump(el.attr)
--   -- el.attributes["placement"] = "H"  -- 'H' means "here"
--   return el
-- end

-- Replace <a id=""></a> style anchors to LaTeX anchors.
-- function RawInline(el)
--   if el.format == "html" then
--     local id = el.text:match('<a id="([^"]+)"%s*/?>')
--     if id then
--       local sanitised = id:gsub("[^%w-]", "-")
--       return pandoc.Span("", {id = sanitised})
--     end
--   end
-- end