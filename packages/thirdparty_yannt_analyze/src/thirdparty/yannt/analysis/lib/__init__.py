#!/usr/bin/env python3

class AnalysisFactor:
    pass


class AnalysisProcess:
    pass


class AnalysisReport:
    pass


class _AnalysisFramework:
    def __init__(self):
        self._formats = {}
        self._factors = {}
        self._processes = {}
        self._reports = {}


    def register_format(self, name: str, fmt: AnalysisFactor):
        self._formats[name] = fmt
        return self

    def register_factor(self, name: str, factor: AnalysisFactor):
        self._factors[name] = factor
        return self

    def register_process(self, name: str, process: AnalysisProcess):
        self._processes[name] = process
        return self

    def register_report(self, name: str, report: AnalysisReport):
        self._reports[name] = report
        return self

AnalysisFramework = _AnalysisFramework()