

from thirdparty.yannt.analysis.lib import (
    AnalysisFactorKey,
    AnalysisFactorRegistry,
    AnalysisFactor,
    AnalysisInput,
    AnalysisProcess,
    AnalysisReport,
)

class TensorsFactor(AnalysisFactor):
    def __init__(self, name = "_init", dependencies = []):
        super().__init__(name=name, dependencies=dependencies)


class GraphFactor(AnalysisFactor):
    def __init__(self, name = "_init", dependencies = []):
        super().__init__(name=name, dependencies=dependencies)

class TensorsMetrics(AnalysisFactor):
    def __init__(self, name = "_init", dependencies = []):
        super().__init__(name=name, dependencies=dependencies)

class FineTuned(AnalysisFactor):
    def __init__(self, name = "_init", dependencies = []):
        super().__init__(name=name, dependencies=dependencies)

class BasicProcess(AnalysisProcess):
    def __init__(self):
        super().__init__()

class FineTunedReport(AnalysisReport):
    def report(self):
        return {'fine_tuned': self._process.results['fine_tuned']}


class TensorMetricsReport(AnalysisReport):
    def __init__(self):
        pass


'''
    # SEE pparse.py
    class PparseFormat(AnalysisInput):
        def __init__(self, name = "_init", dependencies = []):
            super().__init__(name=name, dependencies=dependencies)
            self._arg_parser = self._build_parser()

        def _build_parser(self):
            import argparse
            parser = argparse.ArgumentParser(
                prog="--format onnx",
                description="Derives statistical properties of all tensors in the model",
                formatter_class=argparse.ArgumentDefaultsHelpFormatter
            )
            parser.add_argument("--depth", type=int, default=3, help="Depth of tensor analysis")
            parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
            return parser
        
        def get_parser(self):
            return self._arg_parser
        
        def parse_args(self, opts):
            # Convert the passed (key=value) option dictionary to argparse as argv
            argv = []
            parser = self.get_parser()
            for k, v in opts.items():
                argv.append(f"--{k}")
                if v is not None and v != "":
                    argv.append(str(v))
            return parser.parse_args(argv)
'''


def pparse_plugin(cls_name):
    return ('thirdparty.yannt.analysis.pparse.plugin', cls_name)


def register_analysis_plugin(framework):

    #from thirdparty.yannt.analysis.pparse import PparseFormat
    #config = { 'registry': { 'onnx': 'pparse.onnx', 'pytoroch': 'pparse.pytorch' } }
    #framework.register_factor('pparse', pparse_plugin('PparseFormat'), config)



    # config = { 'registry': { 'onnx': 'pparse.onnx', 'pytoroch': 'pparse.pytorch' } }

    # # ---- Phase 1: Register plugin objects with framework ----
    # # Note: All of these are closured with a config
    # framework.register_factor('pparse', pparse_plugin('PparseFormat'), config)
    # framework.register_factor('tensors', pparse_plugin('TensorsFactor'))
    # framework.register_factor('graph', pparse_plugin('GraphFactor'))
    # framework.register_factor('tensor_metrics', pparse_plugin('TensorsMetrics'))
    # framework.register_factor('fine_tuned', pparse_plugin('FineTuned'))

    # framework.register_report('fine_tuned', pparse_plugin('FineTunedReport'))

    # # ---- Phase 3: Declare the analysis networks ----
    # fine_tuned_proc = framework.create_procedure(name='fine_tuned')
    # fine_tuned_proc.add_input('model_a', factor='pparse')
    # fine_tuned_proc.add_input('model_b', factor='pparse')

    # fine_tuned_proc.add_factor('tensors_a', factor='tensors', dependencies=['model_a'])
    # fine_tuned_proc.add_factor('graph_a', factor='graph', dependencies=['model_a'])
    # fine_tuned_proc.add_factor('tensor_metrics_a', factor='tensor_metrics', dependencies=['tensors_a'])
    # fine_tuned_proc.add_factor('tensors_b', factor='tensors', dependencies=['model_b'])
    # fine_tuned_proc.add_factor('graph_b', factor='graph', dependencies=['model_b'])
    # fine_tuned_proc.add_factor('tensor_metrics_b', factor='tensor_metrics', dependencies=['tensors_b'])

    # fine_tuned_deps = ['tensor_metrics_a', 'tensor_metrics_b', 'graph_a', 'graph_b']
    # fine_tuned_proc.add_factor('fine_tuned', factor='fine_tuned', dependencies=fine_tuned_deps)



    pass







