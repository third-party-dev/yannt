import argparse
from importlib.metadata import entry_points
from typing import Any

from thirdparty.yannt.analysis.lib import FRAMEWORKS, AnalysisFramework
from thirdparty.yannt.analysis.lib.config import Config


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
def register_yannt_analyze(subparsers: Any) -> None:

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
        ep.load()(FRAMEWORKS)


    analyze_parser = subparsers.add_parser("analyze", help="analyze command")
    analyze_parser.add_argument("--breakpoint",
        dest="breakpoint",
        action="store_true",
        help="breakpoint() after operation"
    )
    analyze_parser.add_argument("--test", action="store_true", help="simple developer only test")
    analyze_parser.add_argument("--config", help="config.yaml")

    '''
        Load a factor class:
        --load factor:name=pparse,mod=thirdparty.yannt.analysis.pparse.plugin,cls=PparseFormat

        Load a report class:
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
        Add input to a procedure:
        --factor input:proc=fine_tuned,name=model_a,factor=pparse

        Add a worker to a procedure:
        --factor worker:proc=fine_tuned,name=tensors_a,factor=tensors,dependency=model_a
    '''
    analyze_parser.add_argument(
        "--factor",
        action="append",
        type=parse_process_arg,
        metavar="NAME[:key=value,...]",
        help="Create and populate analysis procedures."
    )

    '''
        Create a process request:
        --request process:proc=fine_tuned,name=fine_tuned

        Create a report request:
        --request report:proc=fine_tuned,name=fine_tuned
    '''
    analyze_parser.add_argument(
        "--request",
        action="append",
        type=parse_process_arg,
        metavar="NAME[:key=value,...]",
        help="Create user request."
    )

    '''
        Assign an input to a process:
        --input process:name=fine_tuned,factor=model_a,path=model.onnx

        Assign an input to a report:
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

def process_config(config: Config) -> None:
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


def do_simple_test() -> None:
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


def handle_load_args(load_args: list[tuple[str, dict]]) -> None:

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
                raise Exception(f"--factor missing a name (--load factor:name=name_here).")
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


def handle_factor_args(factor_args: list[tuple[str, dict]]) -> None:

    '''
        When adding factors (inputs and workers) to procedures, there is no configuration. All factor configuration
        is bound at the loading phase. Factors are stored in the procedure as class objects (not object instances)
        and therefore have no state themselves. The only thing factors can build on across multiple arguments are 
        dependencies and reset of factor_class. This operation is only additive. If there is no framework (fw) 
        specified, default is used.
    '''

    procedures = {}

    # May (overwrite) existing procedure classes.
    for cat, opts in factor_args:
        if cat not in ['input', 'worker']:
            raise Exception(f"--factor must be input or worker, not {cat}.")
        if cat == 'input':
            if 'name' not in opts:
                raise Exception(f"--factor missing a name (--factor input:proc=procedure_here,name=name_here).")
            if 'proc' not in opts:
                raise Exception(f"--factor missing procedure (--factor input:proc=procedure_here,name=name_here).")

            framework_name = opts.pop('fw', 'default')
            procedure_name = opts.pop('proc')
            factor_name = opts.pop('name')

            procedure_entry = procedures.setdefault(procedure_name, {'fw': framework_name, 'inputs': {}, 'workers': {}})
            factor_entry = procedure_entry['inputs'].setdefault(factor_name, {'name': factor_name, 'factor_class': None})
            
            for key, value in opts.items():
                if key == 'factor':
                    # Last write wins
                    factor_entry['factor_class'] = value
                    continue
                #if key == 'dependency' and value not in factor_entry['dependency']:
                #    factor_entry['dependency'].append(value)
                #    continue
                if key == 'dependency':
                    msg = f"Found --factor input:procedure={procedure_name},name={factor_name} " \
                          f"with dependencies. Inputs have no dependencies."
                    raise Exception(msg)

                raise Exception(f"--factor input only accepts fw, proc, and name as options. Not {key}.")
                # opt = factor_entry['opts'].setdefault(key, [])
                # # De-dup for now. Not sure if this is desired.
                # if value not in opt:
                #     opt.append(value)

        if cat == 'worker':
            if 'name' not in opts:
                raise Exception(f"--factor missing a name (--factor worker:proc=procedure_here,name=name_here).")
            if 'proc' not in opts:
                raise Exception(f"--factor missing procedure (--factor worker:proc=procedure_here,name=name_here).")

            framework_name = opts.pop('fw', 'default')
            procedure_name = opts.pop('proc')
            factor_name = opts.pop('name')

            procedure_entry = procedures.setdefault(procedure_name, {'fw': framework_name, 'inputs': {}, 'workers': {}})
            init_factor_entry = {'name': factor_name, 'factor_class': None, 'dependencies': []}
            factor_entry = procedure_entry['workers'].setdefault(factor_name, init_factor_entry)
            
            for key, value in opts.items():
                if key == 'factor':
                    # Last write wins
                    factor_entry['factor_class'] = value
                    continue
                if key == 'dependency' and value not in factor_entry['dependency']:
                    factor_entry['dependency'].append(value)
                    continue

                raise Exception(f"--factor worker only accepts fw, proc, name, and dependency as options. Not {key}.")
                # opt = factor_entry['opts'].setdefault(key, [])
                # # De-dup for now. Not sure if this is desired.
                # if value not in opt:
                #     opt.append(value)
    
    # Sanity check the procedures.
    # Verify worker has deps, verify factor_class defined.
    for procedure_name, procedure_entry in procedures.items():
        for factor_name, factor_entry in procedure_entry['inputs'].items():
            if not isinstance(factor_entry['factor_class'], str):
                raise Exception(f"factor input {factor_name} missing factor_class")
        for factor_name, factor_entry in procedure_entry['workers'].items():
            if not isinstance(factor_entry['factor_class'], str):
                raise Exception(f"factor worker {factor_name} missing factor_class")
            if len(factor_entry['dependencies']) == 0:
                raise Exception(f"factor worker {factor_name} missing dependencies")

    # Apply the new procedures
    for procedure_name, procedure_entry in procedures.items():
        framework = FRAMEWORKS[procedure_entry['fw']]
        # Get existing procedure or create new one
        procedure = framework.procedure.setdefault(procedure_name, framework.create_procedure(name=procedure_name))

        for input_name, input_entry in procedure_entry['inputs'].items():
            procedure._force_add_input(input_name, input_entry['factor_class'])

        for worker_name, worker_entry in procedure_entry['workers'].items():
            procedure._force_add_factor(worker_name, worker_entry['factor_class'], dependencies=worker_entry['dependencies'])


def handle_request_input_args(request_args: list[tuple[str, dict]], input_args: list[tuple[str, dict]]) -> tuple[dict, dict]:
    requests = {}
    #requests = 

    # --- First process requests, so we can apply inputs to something. ---
    # May overwrite process and report classes.
    for cat, opts in request_args:
        if cat not in ['process', 'report']:
            raise Exception(f"--request must be process or report, not {cat}.")
        if cat == 'process':
            if 'name' not in opts:
                raise Exception(f"--request process missing a name (--request process:name=name_here,proc=procedure_here).")
            if 'proc' not in opts:
                raise Exception(f"--request process missing a procedure (--request process:name=name_here,proc=procedure_here).")

            framework_name = opts.pop('fw', 'default')
            framework_entry = requests.setdefault(framework_name, {'processes': {}, 'reports': {}})

            process_name = opts.pop('name')
            procedure_name = opts.pop('proc')
            init_process_entry = {'fw': framework_name, 'name': process_name, 'procedure': procedure_name, 'inputs': {}}
            process_entry = framework_entry['processes'].setdefault(process_name, init_process_entry)

            for key, value in opts.items():
                raise Exception(f"--request input only accepts fw, proc, and name as options. Not {key}.")

        if cat == 'report':
            if 'name' not in opts:
                raise Exception(f"--request report missing a name (--request report:name=name_here,report=procedure_here).")
            if 'proc' not in opts:
                raise Exception(f"--request report missing a procedure (--request report:name=name_here,proc=procedure_here).")
            if 'report' not in opts:
                raise Exception(f"--request report missing a report class (--request report:name=name_here,report=report_class_here).")

            framework_name = opts.pop('fw', 'default')
            framework_entry = requests.setdefault(framework_name, {'processes': {}, 'reports': {}})

            report_name = opts.pop('name')
            report_class = opts.pop('report')
            procedure_name = opts.pop('proc')
            init_report_entry = {
                'fw': framework_name,
                'name': report_name,
                'report_class': report_class,
                'procedure': procedure_name,
                'inputs': {}
            }
            report_entry = framework_entry['reports'].setdefault(report_name, init_report_entry)

            for key, value in opts.items():
                raise Exception(f"--request report only accepts fw, report, and name as options. Not {key}.")

    # --- Now assign all inputs to existing request entries. ---
    for cat, opts in input_args:
        if cat not in ['process', 'report']:
            raise Exception(f"--input must be process or report, not {cat}.")

        if 'name' not in opts:
            raise Exception(f"--input {cat} missing a name (--input {cat}:name=name_here,factor=factor_here).")
        if 'factor' not in opts:
            raise Exception(f"--input {cat} missing a factor (--request {cat}:name=name_here,factor=factor_here).")
        
        if cat == 'process':

            framework_name = opts.pop('fw', 'default')
            # ** Inputs args only apply to CLI requests.
            if framework_name not in requests:
                raise Exception(f"During --input process, no request in specified framework {framework_name}.")
            framework_entry = requests[framework_name]
            process_name = opts.pop('name')
            factor_name = opts.pop('factor')

            if process_name not in framework_entry['processes']:
                raise Exception(f"During --input process, process {process_name} not defined.")
            process_entry = framework_entry['processes'][process_name]

            input_entry = process_entry['inputs'].setdefault(factor_name, {})

            for key, value in opts.items():
                opt = input_entry.setdefault(key, [])
                if value not in opt:
                    opt.append(value)

        if cat == 'report':

            framework_name = opts.pop('fw', 'default')
            # ** Inputs args only apply to CLI requests.
            if framework_name not in requests:
                raise Exception(f"During --input report, no request in specified framework {framework_name}.")
            framework_entry = requests[framework_name]
            report_name = opts.pop('name')
            factor_name = opts.pop('factor')

            if report_name not in framework_entry['reports']:
                raise Exception(f"During --input report, report {report_name} not defined.")
            report_entry = framework_entry['reports'][report_name]

            input_entry = report_entry['inputs'].setdefault(factor_name, {})

            for key, value in opts.items():
                opt = input_entry.setdefault(key, [])
                if value not in opt:
                    opt.append(value)
    
    # TODO: Verify request proc and report's exist in FRAMEWORKS?
    # TODO: Verify all input is satisfied.

    # --- Now create requests and assign inputs. ---
    processes = {}
    reports = {}
    for framework_name, framework_entry in requests.items():
        framework = FRAMEWORKS[framework_name]
        for process_name, process_entry in framework_entry['processes'].items():
            process_fwname = f"{framework_name}-{process_name}"
            processes[process_fwname] = framework.procedure[process_entry['procedure']].create_process()
            for factor_name, factor_entry in process_entry['inputs'].items():
                processes[process_fwname].set_input(factor_name, factor_entry)
        
        # TODO: Describe how does report requiring a procedure make sense?
        for report_name, report_entry in framework_entry['reports'].items():
            report_fwname = f"{framework_name}-{report_name}"
            reports[report_fwname] = framework.init_report(name=report_entry['report'], procedure=report_entry['procedure'])
            for factor_name, factor_entry in report_entry['inputs'].items():
                reports[report_fwname].set_input(factor_name, factor_entry)

    return processes, reports


def do_analysis(args: argparse.Namespace) -> None:
    '''
        Order of precedence (least to most):
            - Hard coded defaults
            - Installed defaults (entry points)
            - Config File
            - Environment Variables
            - CLI Arguments
    '''

    if args.config:
        from thirdparty.yannt.analysis.lib.config import load_config
        process_config(load_config(args.config))

    # ---- Load the factor and report classes from --load args. ----
    if args.load:
        handle_load_args(args.load)

    # ---- Create or update procedures from --factor args. ----
    if args.factor:
        handle_factor_args(args.factor)

    # ---- Create processes (and reports) in CLI ----
    if args.request:
        processes, reports = handle_request_input_args(args.request, args.input)

        '''
            Quick dumb test:

            yannt analyze --breakpoint --config config.yaml \
                --request process:name=mine,proc=fine_tuned \
                --input process:name=mine,factor=model_a,path=model.onnx \
                --input process:name=mine,factor=model_b,path=model.bin

            (Pdb) processes['default-mine'].results
        '''

        # ---- Run processes and reports. ----
        # TODO: Optionally merge the procedures and execute as a single tree here.
        # TODO: Consider allowing a requests section in config.yaml (or requests.yaml)
        # TODO:   and supply it via a --request with_yaml:path=request.yaml argument.

        for process_name, process in processes.items():
            process.run()

        for report_name, report in reports.items():
            report.process()

    if args.test:
        import yaml
        from dataclasses import asdict
        # from pprint import pprint
        with open('tchar_a.txt', 'w') as f:
            # pprint(processes['default-mine'].results['tensor_character_a'], stream=f)
            yaml.dump(asdict(processes['default-mine'].results['tensor_character_a']), stream=f)
        with open('tchar_b.txt', 'w') as f:
            # pprint(processes['default-mine'].results['tensor_character_b'], stream=f)
            yaml.dump(asdict(processes['default-mine'].results['tensor_character_b']), stream=f)
        #do_simple_test()

    if args.breakpoint:
        print(f"Locals: {list(locals().keys())}")
        breakpoint()