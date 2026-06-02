

from thirdparty.yannt.analysis.lib import AnalysisFactor, AnalysisProcess, AnalysisReport


class OnnxFormat(AnalysisFactor):
    def __init__(self):
        self.build_parser()

    def build_parser(self):
        import argparse
        self._arg_parser = argparse.ArgumentParser(
            prog="tensors",
            description="Derives statistical properties of all tensors in the model",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        self._arg_parser.add_argument("--depth", type=int, default=3, help="Depth of tensor analysis")
        self._arg_parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
        return self._arg_parser


class TensorsFactor(AnalysisFactor):
    pass


class BasicProcess(AnalysisProcess):
    pass


class TensorMetricsReport(AnalysisReport):
    pass


def register_analysis_plugin(framework):
    framework.register_format('onnx', OnnxFormat())
    framework.register_factor('tensors', TensorsFactor())
    framework.register_process('basic', BasicProcess())
    framework.register_report('tensor_metrics', TensorMetricsReport())
