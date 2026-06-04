from importlib.metadata import entry_points
from thirdparty.yannt.analysis.lib import AnalysisFramework


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
        ep.load()(AnalysisFramework)


    analyze_parser = subparsers.add_parser("analyze", help="analyze command")
    analyze_parser.add_argument("--breakpoint",
        dest="breakpoint",
        action="store_true",
        help="breakpoint() after operation"
    )
    # analyze_parser.add_argument(
    #     "--format",
    #     action="append",
    #     type=parse_process_arg,
    #     metavar="NAME[:key=value,...]",
    #     help="Analysis process to run, with optional configuration"
    # )
    analyze_parser.add_argument(
        "--factor",
        action="append",
        type=parse_process_arg,
        metavar="NAME[:key=value,...]",
        help="Analysis process to run, with optional configuration"
    )
    # analyze_parser.add_argument(
    #     "--process",
    #     action="append",
    #     type=parse_process_arg,
    #     metavar="NAME[:key=value,...]",
    #     help="Analysis process to run, with optional configuration"
    # )
    # analyze_parser.add_argument(
    #     "--report",
    #     action="append",
    #     type=parse_process_arg,
    #     metavar="NAME[:key=value,...]",
    #     help="Report to generate, with optional configuration"
    # )
    # analyze_parser.add_argument(
    #     "--format-help",
    #     choices=list(AnalysisFramework._formats.keys()),
    #     metavar="NAME",
    #     help=f"Show help for a process. Available: {', '.join(AnalysisFramework._formats.keys())}"
    # )
    analyze_parser.add_argument(
        "--factor-help",
        choices=list(AnalysisFramework._factors.keys()),
        metavar="NAME",
        help=f"Show help for a process. Available: {', '.join(AnalysisFramework._factors.keys())}"
    )
    # analyze_parser.add_argument(
    #     "--process-help",
    #     choices=list(AnalysisFramework._processes.keys()),
    #     metavar="NAME",
    #     help=f"Show help for a process. Available: {', '.join(AnalysisFramework._processes.keys())}"
    # )
    # analyze_parser.add_argument(
    #     "--report-help",
    #     choices=list(AnalysisFramework._reports.keys()),
    #     metavar="NAME",
    #     help=f"Show help for a process. Available: {', '.join(AnalysisFramework._reports.keys())}"
    # )
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


def do_analysis(args):

    # if args.format_help:
    #     print_process_help(args.format_help, 'format', AnalysisFramework._formats[args.format_help])
    
    # if args.format:
    #     format_args = _dedup_name_key_val(args.format)
    #     AnalysisFramework._formats[args.format_help].parse_args(format_args[])


    # `yannt analyze --format onnx:depth=123,another=435 --format onnx:depth=2`

    print("--- Loaded Analysis Framework Features ---")

    print("Registered factors:")
    for factor_key, factor_cls in AnalysisFramework.factor.items():
        print(f"  - {factor_key} => {factor_cls.__module__}:{factor_cls.__name__}")

    print("Registered procedures:")
    for procedure_key, procedure in AnalysisFramework.procedure.items():
        print(f"  - {procedure_key}: {procedure.__class__}")

    print("--- Merged Process Execution ---")
    
    process = AnalysisFramework.procedure['fine_tuned'].create_process()
    process.set_input('model_a', "model.onnx")
    process.set_input('model_b', "model.bin")
    process.run()

    print("--- Merged Process Results ---")
    from pprint import pprint
    pprint(dict(process.results))

    print("--- init_report Results ---")

    report = AnalysisFramework.init_report('fine_tuned', procedure='fine_tuned')
    report.set_input('model_a', "model.onnx")
    report.set_input('model_b', "model.bin")
    report.process()
    print("REPORT:")
    pprint(dict(report.results))
    

    print("--- post_process_report Results ---")

    report = AnalysisFramework.post_process_report('fine_tuned', process=process)
    print("REPORT:")
    pprint(dict(report.results))