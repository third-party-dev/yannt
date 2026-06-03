

from thirdparty.yannt.analysis.lib import (
    AnalysisFactorKey,
    AnalysisFactorRegistry,
    AnalysisFactor,
    AnalysisProcess,
    AnalysisReport,
)

class OnnxFormat(AnalysisFactor):
    def __init__(self, _id = "_init", dependencies = []):
        super().__init__(_id=_id, dependencies=dependencies)
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


class TensorsFactor(AnalysisFactor):
    def __init__(self, _id = "_init", dependencies = []):
        super().__init__(_id=_id, dependencies=dependencies)


class BasicProcess(AnalysisProcess):
    def __init__(self):
        super().__init__()


    


class TensorMetricsReport(AnalysisReport):
    def __init__(self):
        pass


def register_analysis_plugin(framework):
    framework.register_format('onnx', OnnxFormat())
    framework.register_factor('tensors', TensorsFactor())
    basic = BasicProcess()
    framework.register_process('basic', basic)
    framework.register_report('tensor_metrics', TensorMetricsReport())

    basic.register_factor(TensorsFactor(_id="_init", dependencies=[(OnnxFormat, "_init")]))
    basic.register_factor(OnnxFormat(_id="_init"))










