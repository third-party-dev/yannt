

from typing import Any

from thirdparty.yannt.analysis.lib import (
    AnalysisFactorKey,
    AnalysisFactorRegistry,
    AnalysisFactor,
    AnalysisFramework,
    AnalysisInput,
    AnalysisProcess,
    AnalysisReport,
)



class TensorsMetrics(AnalysisFactor):
    def __init__(self, name: str = "_init", dependencies: list = []) -> None:
        super().__init__(name=name, dependencies=dependencies)

class FineTuned(AnalysisFactor):
    def __init__(self, name: str = "_init", dependencies: list = []) -> None:
        super().__init__(name=name, dependencies=dependencies)

class BasicProcess(AnalysisProcess):
    def __init__(self) -> None:
        super().__init__()

class FineTunedReport(AnalysisReport):
    def report(self) -> dict:
        return {'fine_tuned': self._process.results['fine_tuned']}


class TensorMetricsReport(AnalysisReport):
    def __init__(self) -> None:
        pass


def pparse_plugin(cls_name: str) -> tuple[str, str]:
    return ('thirdparty.yannt.analysis.pparse.plugin', cls_name)


def register_analysis_plugin(framework: AnalysisFramework) -> None:

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







