from importlib.metadata import entry_points
from thirdparty.yannt.analysis.lib import FRAMEWORKS, AnalysisFramework


def parse_process_arg(value: str) -> tuple[str, dict]:
    if ":" not in value:
        return value, {}
    name, opts_str = value.split(":", 1)
    opts = {}
    for pair in opts_str.split(","):
        pair = pair.strip()
        if not pair:
            continue
        if "=" not in pair:
            # No value — treat as boolean flag
            opts[pair] = True
        else:
            k, v = pair.split("=", 1)
            opts[k.strip()] = v.strip()
    return name, opts


# Function called my yannt based on yannt_command entrypoint registration in pyproject.toml
def register_yannt_analyze(subparsers):

    '''
        Order of precedence (least to most):
            - Hard coded defaults
            - Installed defaults (entry points)
            - Config File
            - Environment Variables
            - CLI Arguments
    '''

    # TODO: Load all the entrypoints and populate the framework.
    if isinstance(entry_points(), dict):
        # Python <3.10
        eps = []
        if 'yannt_analysis_plugin' in entry_points():
            for ep in entry_points()['yannt_analysis_plugin']:
                if not ep in eps:
                    eps.append(ep)
    else:
        # Python >=3.10
        eps = entry_points(group="yannt_analysis_plugin")

    for ep in eps:
        ep.load()(FRAMEWORKS['default'])


    analyze_parser = subparsers.add_parser("analyze", help="analyze command")
    analyze_parser.add_argument("--breakpoint",
        dest="breakpoint",
        action="store_true",
        help="breakpoint() after operation"
    )
    analyze_parser.add_argument("--test", action="store_true", help="simple developer only test")
    analyze_parser.add_argument("--config", help="config.yaml")

    '''
        TODO: Load a factor class
        --load factor:name=pparse,mod=thirdparty.yannt.analysis.pparse.plugin,cls=PparseFormat

        TODO: Load a report class
        --load report:name=fine_tuned,mod=thirdparty.yannt.analysis.pparse.plugin,cls=FineTunedReport
    '''
    analyze_parser.add_argument(
        "--load",
        action="append",
        type=parse_process_arg,
        metavar="NAME[:key=value,...]",
        help="Load factor and report classes into framework."
    )

    '''
        TODO: Add input to a procedure.
        --factor input:procedure=fine_tuned,name=model_a,factor=pparse

        TODO: Add a worker to a procedure.
        --factor worker:procedure=fine_tuned,name=tensors_a,factor=tensors,dependency=model_a
    '''
    analyze_parser.add_argument(
        "--factor",
        action="append",
        type=parse_process_arg,
        metavar="NAME[:key=value,...]",
        help="Create and populate analysis procedures."
    )

    '''
        TODO: Create a process request
        --request process:procedure=fine_tuned,name=fine_tuned

        TODO: Create a report request
        --request report:procedure=fine_tuned,name=fine_tuned
    '''
    analyze_parser.add_argument(
        "--request",
        action="append",
        type=parse_process_arg,
        metavar="NAME[:key=value,...]",
        help="Create user request."
    )

    '''
        TODO: Assign an input to a process
        --input process:name=fine_tuned,factor=model_a,path=model.onnx

        TODO: Assign an input to a report
        --input report:name=fine_tuned,factor=model_b,path=model.bin
    '''
    analyze_parser.add_argument(
        "--input",
        action="append",
        type=parse_process_arg,
        metavar="NAME[:key=value,...]",
        help="Assign inputs to user requests."
    )


    '''
        TODO: Get description of how these categories work.
        --load-help factor
        --load-help report

        TODO: Get descriptions of classes.
        --load-help factor:mod=thirdparty.yannt.analysis.pparse.plugin,cls=PparseFormat
        --load-help report:mod=thirdparty.yannt.analysis.pparse.plugin,cls=FineTunedReport

        TODO: List all the loaded classes
        --load-list

        TODO: List all the loaded factor classes
        --load-list factor

        TODO: List all the loaded report classes
        --load-list report

        TODO:
        --factor-help input

        TODO:
        --factor-help worker

        TODO: Show help associated with class named 'factor'
        --factor-help input:factor=pparse

        TODO: Show help associated with class named 'factor'
        --factor-help worker:factor=tensors

        TODO: List summary of all factors in procedure
        --factor-list procedure=fine_tuned

        TODO: List summary of all input factors in procedure
        --factor-list input:procedure=fine_tuned

        TODO: List summary of all worker factors in procedure
        --factor-list worker:procedure=fine_tuned

        TODO:
        -request-help process

        TODO:
        -request-help report

        TODO: summary of process (and inputs)
        --request-help process:name=fine_tuned

        TODO: summary of report (and inputs)
        --request-help report:name=fine_tuned

        TODO: list summary of processes (and inputs)
        --request-list process

        TODO: list summary of reports (and inputs)
        --request-list report

        TODO: Get summary of available options
        --input-help process:name=fine_tuned,factor=model_a
        --input-list process:name=fine_tuned,factor=model_a

        TODO: Get summary of available options
        --input-help report:name=fine_tuned,factor=model_b
        --input-list report:name=fine_tuned,factor=model_b

        analyze_parser.add_argument(
            "--thing-help",
            type=parse_process_arg,
            metavar="NAME[:key=value,...]",
            help=f"Show help for a process. Available: {', '.join(FRAMEWORKS['default']._factors.keys())}"
        ) 
    '''
    analyze_parser.set_defaults(func=do_analysis)


# def print_process_help(obj):
#     import argparse
#     parser = obj.get_parser()
#     formatter = process_parser._get_formatter()
    
#     formatter.add_usage(f"{parser.prog}[:key=value,...]", [], [], prefix="Usage: ")
#     formatter.add_text(parser.description)
    
#     # harvest option groups directly from the process parser
#     formatter.start_section("Options")
#     for action in parser._actions:
#         if isinstance(action, argparse._HelpAction):
#             continue
#         # reformat as key=value instead of --key VALUE
#         breakpoint()
#         option = f"{action.dest}={action.metavar or action.type.__name__ if action.type else 'value'}"
#         formatter.add_text(f"  {option:<30} {action.help} (default: {action.default})")
#     formatter.end_section()
    
#     print(formatter.format_help())


# def _dedup_name_key_val(params: list[tuple[str, dict]]) -> list[tuple[str, dict]]:
#     result = {}
#     for name, opts in params:
#         result.setdefault(name, {})
#         result[name] = {**result[name], **opts}
#     return result


# _dedup_name_key_val(args.format or [])

def process_config(config):
    for framework_config in config.frameworks:
        framework = FRAMEWORKS.setdefault(framework_config.name, AnalysisFramework(name=framework_config.name))
        # ** Note: overwriting any entry point registrations and hard coded defaults.

        # Load factors classes.
        for factor_class in framework_config.factor_classes:
            factor_desc = (factor_class.module, factor_class.klass)
            framework._force_register_factor(factor_class.name, factor_desc, config=factor_class.config)
        
        # Load report classes.
        for report_class in framework_config.report_classes:
            report_desc = (report_class.module, report_class.klass)
            framework._force_register_report(report_class.name, report_desc, config=report_class.config)

        # Create procedures.
        for procedure_entry in framework_config.procedures:
            procedure = framework.create_procedure(name=procedure_entry.name)

            # Dynamically subclass and name inputs
            for inp_factor in procedure_entry.input_factors:
                procedure.add_input(inp_factor.name, factor=inp_factor.factor_class)

            # Dynamically subclass and name factors
            for worker in procedure_entry.worker_factors:
                procedure.add_factor(worker.name, factor=worker.factor_class, dependencies=worker.dependencies)


def do_simple_test():
    print("--- Loaded Analysis Framework Features ---")

    print("Registered factors:")
    for factor_key, factor_cls in FRAMEWORKS['default'].factor.items():
        print(f"  - {factor_key} => {factor_cls.__module__}:{factor_cls.__name__}")

    print("Registered procedures:")
    for procedure_key, procedure in FRAMEWORKS['default'].procedure.items():
        print(f"  - {procedure_key}: {procedure.__class__}")

    print("--- Merged Process Execution ---")
    
    process = FRAMEWORKS['default'].procedure['fine_tuned'].create_process()
    process.set_input('model_a', "model.onnx")
    process.set_input('model_b', "model.bin")
    process.run()

    print("--- Merged Process Results ---")
    from pprint import pprint
    pprint(dict(process.results))

    print("--- init_report Results ---")

    report = FRAMEWORKS['default'].init_report('fine_tuned', procedure='fine_tuned')
    report.set_input('model_a', "model.onnx")
    report.set_input('model_b', "model.bin")
    report.process()
    print("REPORT:")
    pprint(dict(report.results))
    

    print("--- post_process_report Results ---")

    report = FRAMEWORKS['default'].post_process_report('fine_tuned', process=process)
    print("REPORT:")
    pprint(dict(report.results))


def handle_load_args(load_args):

    to_load = {
        'factor_classes': {},
        'report_classes': {},
    }

    # Load (overwrite) factor and report classes.
    for cat, opts in load_args:
        if cat not in ['factor', 'report']:
            raise Exception(f"--load must be factor or report, not {cat}.")
        if cat == 'factor':
            if 'name' not in opts:
                raise Exception(f"--load missing a name (--load factor:name=name_here).")
            factor_name = opts.pop('name')
            factor_class_entry = to_load['factor_classes'].setdefault(factor_name, {'mod':None, 'cls':None, 'config': {}})
            
            for key, value in opts.items():
                if key == 'mod':
                    factor_class_entry['mod'] = value
                    continue
                if key == 'cls':
                    factor_class_entry['cls'] = value
                    continue

                opt = factor_class_entry['config'].setdefault(key, [])
                # De-dup for now. Not sure if this is desired.
                if value not in opt:
                    opt.append(value)

        if cat == 'report':
            if 'name' not in opts:
                raise Exception(f"--load missing a name (--load report:name=name_here).")
            report_name = opts.pop('name')
            report_class_entry = to_load['report_classes'].setdefault(report_name, {'mod':None, 'cls':None, 'config': {}})

            for key, value in opts.items():
                if key == 'mod':
                    report_class_entry['mod'] = value
                    continue
                if key == 'cls':
                    report_class_entry['cls'] = value
                    continue

                opt = report_class_entry['config'].setdefault(key, [])
                # De-dup for now. Not sure if this is desired.
                if value not in opt:
                    opt.append(value)
    
    # Sanity check the to_load for mod and cls values.
    for factor_name, factor_class in to_load['factor_classes'].items():
        if not factor_class['mod']:
            raise Exception(f"--load factor:name={factor_name} missing required mod.")
        if not factor_class['cls']:
            raise Exception(f"--load factor:name={factor_name} missing required cls.")

    for report_name, report_class in to_load['report_classes'].items():
        if not report_class['mod']:
            raise Exception(f"--load report:name={report_name} missing required mod.")
        if not report_class['cls']:
            raise Exception(f"--load report:name={report_name} missing required cls.")

    # Do the loads
    for factor_name, factor_class in to_load['factor_classes'].items():
        # TODO: Allow framework selection in options.
        FRAMEWORKS['default']._force_register_factor(factor_name, (factor_class['mod'], factor_class['cls']), factor_class['config'])
    
    for report_name, report_class in to_load['report_classes'].items():
        # TODO: Allow framework selection in options.
        FRAMEWORKS['default']._force_register_report(report_name, (report_class['mod'], report_class['cls']), report_class['config'])


def do_analysis(args):

    if args.config:
        '''
            Order of precedence (least to most):
                - Hard coded defaults
                - Installed defaults (entry points)
                - Config File
                - Environment Variables
                - CLI Arguments
        '''

        from thirdparty.yannt.analysis.lib.config import load_config
        process_config(load_config(args.config))

    # ---- Load the factor and report classes from --load args. ---
    if args.load:
        handle_load_args(args.load)

    # TODO: ---- Create or update procedures from --factor args. ---

    breakpoint()
                

    # Load (overwrite) factor and report classes.
    if args.factor:
        for factor_arg in args.factor:
            print(f"factor_arg: {factor_arg}")

    # TODO: ---- Apply the load and factor arguments here. ----

    # TODO: ---- Generate processes and reports entries ----

    # Create processes (and reports) in CLI
    if args.request:
        for request_arg in args.request_arg:
            print(f"request_arg: {request_arg}")

    # Assign inputs to processes from CLI
    if args.input:
        for input_arg in args.input:
            print(f"input_arg: {input_arg}")

    # TODO: ---- Run processes and reports here. ----


    if args.test:
        do_simple_test()

    if args.breakpoint:
        print(f"Locals: {list(locals().keys())}")
        breakpoint()