#!/usr/bin/env python3

'''
    We provide a list of all things to document (exports, explicit nodes). The same list will have a 
    reverse lookup from the simple member name. All of these are put in a flat dictionary of fqns. While 
    documenting classes, functions, or other members, if a member path matches an entry in the fqn 
    database, we add a hyperref as if there will be an anchor. Adding double backticks to a label will
    cause a reverse lookup and hyperref to the fqn anchor in the same way.
'''


from pprint import pprint

import griffe

from typing import Any, Optional

def md_table(rows: list[dict[str, Any]], columns: Optional[list[str]] = None) -> str:
    if not rows:
        return ""
    cols = columns or list(rows[0].keys())

    widths = {c: len(c) for c in cols}
    for row in rows:
        for c in cols:
            widths[c] = max(widths[c], len(str(row.get(c, ""))))

    def fmt_row(values: list[str]) -> str:
        return "| " + " | ".join(v.ljust(widths[c]) for c, v in zip(cols, values)) + " |"

    header = fmt_row(cols)
    separator = "| " + " | ".join("-" * widths[c] for c in cols) + " |"
    body = [fmt_row([str(row.get(c, "")) for c in cols]) for row in rows]

    return "\n".join([header, separator] + body)


def prototype(func) -> str:
    parts = []
    for p in func.parameters:
        if p.name == "self" or p.name == "cls":
            continue

        # prefix for *args and **kwargs
        if p.kind == griffe.ParameterKind.var_positional:
            name = f"*{p.name}"
        elif p.kind == griffe.ParameterKind.var_keyword:
            name = f"**{p.name}"
        elif p.kind == griffe.ParameterKind.keyword_only:
            name = p.name          # caller must add bare * separator
        else:
            name = p.name

        segment = name
        if p.annotation:
            segment += f": {p.annotation}"
            # TODO: Consider adding cross references to annotations that include registered classes
        if p.default:
            segment += f" = {p.default}"

        parts.append(segment)

    returns = f" -> {func.returns}" if func.returns else ""
    return f"def [`{func.name}`](#{func.path})``({', '.join(parts)}){returns}"


def clean_text(text: str, anchor_map: dict) -> str:
    import re

    def resolve(m):
        name = m.group(1)
        if name in anchor_map:
            return f"[`{name}`]({anchor_map[name]})"
        return f"`{name}`"   # fallback to plain code if not found

    text = re.sub(r'``(.+?)``', resolve, text)
    return text

def render_class(fqns, bigscope, restrictions, klass):
    # print(f"Class Name: {item['alias']}") # item_api.name
    # print(f"Class FQN: {item['fqn']}") # item_api.path

    klass_name = klass.name
    bases = ', '.join([base.name for base in klass.bases])
    decorators = [f"@{str(d.value)}" for d in klass.decorators]
    members = list(klass.members.keys())

    if klass.path in restrictions:
        restrict = restrictions[klass.path]
        if 'alias' in restrict:
            klass_name = restrict['alias']
        if 'allow_members' in restrict:
            members = restrict['allow_members']
        if 'deny_members' in restrict:
            for deny in restrict['deny_members']:
                if deny in members:
                    member.remove(deny)

    print("--------------------------------------------------------------")
    if len(decorators) > 0:
        for decorator in decorators:
            print(decorator)
        print(f"{klass.kind.value} {klass_name}({bases})")
    else:
        print(f"{klass.kind.value} {klass_name}({bases})")
    print("--------------------------------------------------------------")

    # # Handle docstring
    # print("Class Documentation:")
    # for doc_item in item_api.docstring.parsed:
    #     if doc_item.kind.value == griffe.DocstringSectionKind.text:
    #         '''
    #             TODO: Track all double quotes as explicit references. Need to track this items's 
    #             path with the double back ticked reference for possible scoping resolution.
    #             For now, we can ease the implementation by making any conflicts in alias
    #             space an error and then only add the above resolution after we find a real
    #             world conflict.
    #         '''
    #         print(clean_text(doc_item.value, ()))
    #     else:
    #         breakpoint()

    # Add member table.
    rows = []

    for member_name in members:
        member_api = klass.members[member_name]

        if member_api.kind == griffe.Kind.FUNCTION:
            rows.append({"Prototype": prototype(member_api)})
        elif member_api.kind == griffe.Kind.ATTRIBUTE:
            print(f"Attribute: {member_api.name} = {member_api.value}")
        else:
            print(f"Unknown kind in member table: {member_api.path} {member_api.kind}")
            breakpoint()

    print(md_table(rows))


# --- Do a preliminary inspection of the all the top level things we want to document ---

def main():
    exports_to_load = [
        'thirdparty.pparse.lib'
    ]

    restrictions = {
        'thirdparty.pparse.lib.Node': {
            # Optionally we can replace item.name with explicit alias.?
            #'alias': 'Node',
            # The active entry we're restricting
            'fqn': 'thirdparty.pparse.lib.Node',
            
            # No need yet, but griffe can takes a search_paths
            # 'search_paths': [ { 'path': '.' }, ],

            # deny always wins
            'deny_members': [ '_ctx' ],
            # allow implies limited set
            'allow_members': [
                'clear_ctx',
                'ctx',
                'dump',
                'from_xml',
                'length',
                'load',
                'set_length',
                'tell',
                'unload',
                'value',
            ],
        }
    }

    fqns = {}
    bigscope = {}

    # Load exports
    for export_to_load in exports_to_load:
        fqns[export_to_load] = griffe.load(export_to_load)
        for export_name in fqns[export_to_load].exports:
            export = fqns[export_to_load].members[export_name]
            fqns[export.path] = export



    # Populate Reverse Lookup
    for fqn, member in fqns.items():
        if member.name in bigscope:
            raise Exception(f"Duplicate class name while populated rev lookup: {fqn}")
        bigscope[member.name] = fqn


    # Generate markdown with full anchor map
    for member in fqns.values():
        if member.kind == griffe.Kind.MODULE:
            # TODO: Organize things by module.
            continue
        elif member.kind == griffe.Kind.ATTRIBUTE:
            # TODO: This makes more sense in module context.
            print(f"Attribute: {member.name} = {member.value}")
        elif member.kind == griffe.Kind.CLASS:
            render_class(fqns, bigscope, restrictions, member)
        else:
            print(f"Unknown kind: {member.kind.value}")
            breakpoint()

main()


# to_document = [
#     {
#         'item': {
#             'alias': 'Node',
#             'fqn': 'thirdparty.pparse.lib.Node',
#             # 'search_paths': [ { 'path': '.' }, ],
#             'included_members': [
#                 { 'member': 'clear_ctx' },
#                 { 'member': 'ctx' },
#                 { 'member': 'dump' },
#                 { 'member': 'from_xml' },
#                 { 'member': 'length' },
#                 { 'member': 'load' },
#                 { 'member': 'set_length' },
#                 { 'member': 'tell' },
#                 { 'member': 'unload' },
#                 { 'member': 'value' },
#             ],
#         },
#     },
# ]

# for _item in to_document:
#     item = _item['item']
#     item_api = griffe.load(item['fqn'])

#     if item_api.is_class:
#         render_class(item, item_api)

#     breakpoint()

    