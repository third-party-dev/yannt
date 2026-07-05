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

# --- Do a preliminary inspection of the all the top level things we want to document ---


'''
Three levels: module, namespace, member

Each module gets its own page.

We want the namespace list flat:
'''


def get_namespaces(ns_list = [], p_target = None):
    if p_target is None:
        return ns_list

    target = p_target
    if isinstance(target, str):
        #print(f"Skipping str {target}")
        return ns_list
    if isinstance(target, griffe.Alias):
        try:
            target.resolve_target()
        except Exception as exc:
            #print(f"Skipping alias {target.target_path}")
            return ns_list
        target = target.final_target

    if isinstance(target, griffe.Attribute) or isinstance(target, griffe.Module):
        return ns_list

    if isinstance(target, griffe.Class) or isinstance(target, griffe.Function):
        if len(target.members) > 0:
            print(f"Adding {target.canonical_path} {type(target)}")
            ns_list.append(target)
            for name, member in target.members.items():
                ns_list = get_namespaces(ns_list, member)
    else:
        print(f"Found {type(target)}")
        breakpoint()

    return ns_list

def process_docstring(docstring, member_dict):

    text = []
    parameters = {}
    returns = {}
    raises = {}

    sections = docstring.parse("google")
    for section in sections:
        try:
            if section.kind == griffe.DocstringSectionKind.text:
                text.append(section.value)
            elif section.kind == griffe.DocstringSectionKind.parameters:
                for param_entry in section.value:
                    parameters[str(param_entry.name)] = {
                        'annotation': str(param_entry.annotation),
                        'name': str(param_entry.name),
                        'description': str(param_entry.description),
                        'default': str(param_entry.default),
                    }
            elif section.kind == griffe.DocstringSectionKind.returns:
                for ret_entry in section.value:
                    returns[str(ret_entry.annotation)] = ret_entry.description
            elif section.kind == griffe.DocstringSectionKind.raises:
                for exc_entry in section.value:
                    raises[str(exc_entry.annotation)] = exc_entry.description
            else:
                print(section.kind, section.value)
                breakpoint()
        except Exception as exc:
            import traceback
            traceback.print_exc()
            print(exc)
            breakpoint()
    
    member_dict['docstring'] = {
        'text': ' '.join(text),
        'parameters': parameters,
        'returns': returns,
        'raises': raises,
        # TODO: Add the others
    }


def main():

    fqns = {}
    griffe_exports = {}

    exports_list = ['thirdparty.pparse.lib']
    exports_dict = {}

    # TODO: Consider adding filters or restrictions.

    for fq_export in exports_list:
        export_namespaces = []
        exports_dict[fq_export] = {'griffe': griffe.load(fq_export)}

        for name, g_member in exports_dict[fq_export]['griffe'].members.items():
            exports_dict['namespaces'] = get_namespaces(export_namespaces, g_member)

        ns_dict = {}
        for ns in exports_dict['namespaces']:
            # Populate ns_dict for use as is_namespace lookup.
            ns_dict[ns.canonical_path] = {
                'fqn': ns.canonical_path,
            }

            if hasattr(ns, 'docstring') and ns.docstring is not None:
                process_docstring(ns.docstring, ns_dict[ns.canonical_path])

            # Intentionally added here to have member appear last
            ns_dict[ns.canonical_path]['members'] = {}
        
        # ! TODO: Consider the members that are namespaces. Do we duplicate, defer, skip?

        for ns in exports_dict['namespaces']:
            for name, member in ns.members.items():
                fqn = f'{ns.canonical_path}.{name}'

                # TODO: Generate signature.
                # signature = ''

                ns_dict[ns.canonical_path]['members'][name] = {
                    'fqn': fqn,
                    'is_namespace': fqn in ns_dict,
                }

                # Parse docstring.
                if hasattr(member, 'docstring') and member.docstring is not None:
                    process_docstring(member.docstring, ns_dict[ns.canonical_path]['members'][name])

        # ** At this point ns_dict should be complete an ready for json to markdown conversion.

        # TODO: Control the output path.
        with open(f'{fq_export}-api.json', 'w') as fobj:
            import json
            fobj.write(json.dumps(ns_dict))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(e)
        breakpoint()


