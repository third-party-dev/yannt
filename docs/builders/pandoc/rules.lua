-- rules.lua
--
-- API reference documents need two visually distinct separators:
--   - a THICK rule between namespaces (classes, top-level modules, ...)
--   - a THIN rule between members (functions, attributes, ...) and their
--     member-summary tables.
--
-- Author markup (same in every source file, regardless of target format):
--
--     ::: {.namespace-rule}
--     :::
--
--     ::: {.member-rule}
--     :::
--
-- These are emitted by the API-doc generator (scripts/gen_api_docs.py) but
-- are just as valid hand-written in any regular page.

local FORMAT = FORMAT

local TYPST_THICK = "#line(length: 100%, stroke: 1.6pt)"
local TYPST_THIN  = "#line(length: 100%, stroke: 0.4pt + gray)"

local HTML_THICK = '<hr class="namespace-rule">'
local HTML_THIN  = '<hr class="member-rule">'

function Div(el)
  local isNamespace = el.classes:includes("namespace-rule")
  local isMember     = el.classes:includes("member-rule")
  if not (isNamespace or isMember) then
    return nil
  end

  if FORMAT == "typst" then
    local raw = isNamespace and TYPST_THICK or TYPST_THIN
    return pandoc.RawBlock("typst", raw)
  elseif FORMAT:match("html") then
    local raw = isNamespace and HTML_THICK or HTML_THIN
    return pandoc.RawBlock("html", raw)
  elseif FORMAT:match("commonmark") or FORMAT:match("markdown") then
    -- Raw HTML block passes straight through CommonMark/Docusaurus (MDX
    -- renders bare <hr> tags fine) and still degrades to *** in editors
    -- that don't render raw HTML if you ever inspect the source directly.
    local raw = isNamespace and HTML_THICK or HTML_THIN
    return pandoc.RawBlock("html", raw)
  end

  return nil -- unknown format: leave the empty div as-is rather than guess
end
