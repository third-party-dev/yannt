#!/usr/bin/env python3


from abc import ABC, abstractmethod
from collections import defaultdict, deque
from typing import Any, Union, List


AnalysisFactorKey = tuple[type["AnalysisFactor"], str]
AnalysisFactorRegistry = dict[AnalysisFactorKey, "AnalysisFactor"]
class AnalysisFactor():
    def __init__(self, name='unnamed', dependencies=None):
        # The name of the factor
        self.name = name

        # Note: These dependencies are for reference only, not for sorting.
        self.dependencies = dependencies or []

        self.result_tags = []


    def get_name(self):
        return self.name


    def get_results(self):
        return self._process.results


    def get_result(self, name):
        return self.get_results()[name]


    def run(self):
        pass
        # #from pprint import pprint
        # print(f"Running in {type(self)}:{self.name} with result:")
        # #pprint(dict(process.results))
        # return None


    def __repr__(self):
        return f"{type(self).__name__}(name={self.name!r})"


class AnalysisInput(AnalysisFactor):
    def __init__(self, name='unnamed', dependencies=None):
        super().__init__(name=name, dependencies=dependencies)
        self.input = None


    def get_input(self):
        return self.input


    def missing_input(self):
        return self.input is None


    def set_input(self, inp):
        self.input = inp
        return self


class AnalysisProcess:
    def __init__(self, factor_obj_list):
        self.factor_obj_list = factor_obj_list
        self.factors_objs = defaultdict(dict)
        self.results = defaultdict(dict)
        self.input_factors = {}

        for factor_obj in self.factor_obj_list:
            if isinstance(factor_obj, AnalysisInput):
                self.input_factors[factor_obj.name] = factor_obj
            factor_obj._process = self


    def set_input(self, name, inp):
        self.input_factors[name].set_input(inp)
        return self


    def run(self):
        # Check all input is not None.
        for input_obj in self.input_factors.values():
            if input_obj.missing_input():
                raise Exception(f"Factor {input_obj.name} is missing input.")

        # Do the run
        for factor_obj in self.factor_obj_list:
            self.factors_objs[factor_obj.name] = factor_obj
            self.results[factor_obj.name] = factor_obj.run()

        return self


class AnalysisProcedure:

    def __init__(self, name='unnamed', framework=None):
        self.name = name

        self.framework = framework
        if self.framework is None:
            self.framework = FRAMEWORKS['default']

        self.inputs = {}
        self.factors = {}


    def _force_add_input(self, name, factor):
        if factor not in self.framework.factor:
            raise KeyError(f"Factor {factor} not registered in framework {self.framework.name}.")
        self.inputs[name] = self.framework.factor[factor]
        self._force_add_factor(name, factor)
        return self


    def add_input(self, name, factor):
        if factor not in self.framework.factor:
            raise KeyError(f"Factor {factor} not registered in framework {self.framework.name}.")
        if name in self.inputs:
            raise ValueError(f"Duplicate input name {name} added to process {self.name}.")
        self.inputs[name] = self.framework.factor[factor]
        self.add_factor(name, factor)
        return self


    def _force_add_factor(self, name, factor, dependencies=None):
        if factor not in self.framework.factor:
            raise KeyError(f"Factor {factor} not registered in framework {self.framework.name}.")
        self.factors[name] = (self.framework.factor[factor], dependencies or [])
        return self


    def add_factor(self, name, factor, dependencies=None):
        if name in self.factors:
            raise ValueError(f"Duplicate factor name {name} added to process {self.name}.")
        self._force_add_factor(name, factor, dependencies=dependencies)
        return self

    
    def create_process(self):
        factor_objs = []
        factor_cls_list = self.topo_sorted_factors()
        for factor_name, factor_cls, factor_deps in factor_cls_list:
            factor_obj = factor_cls(name=factor_name, dependencies=factor_deps)
            factor_objs.append(factor_obj)
        
        return AnalysisProcess(factor_objs)


    def topo_sorted_factors(self):
        visited = set()
        visiting = set()
        result = []

        def visit(name):
            if name in visiting:
                raise ValueError(f"Circular dependency at factor {name} in procedure {self.name}.")
            if name in visited:
                return
            visiting.add(name)
            _, dependencies = self.factors[name]
            for dep in dependencies:
                if dep not in self.factors:
                    raise KeyError(f"Factor {name} depends on unknown factor {dep} in procedure {self.name}.")
                visit(dep)
            visiting.discard(name)
            visited.add(name)
            result.append(name)

        for name in self.factors:
            visit(name)

        return [(name, *self.factors[name]) for name in result]
    

    def topo_sorted_levels(self, thread_count: int) -> List[List[tuple]]:
        # Parallel topological sort (BFS) with dependency tree level awareness.
        # Allows multi-threaded distribution of factor processing.

        in_degree = {name: 0 for name in self.factors}
        dependents = {name: [] for name in self.factors}

        for name, (_, dependencies) in self.factors.items():
            for dep in dependencies:
                if dep not in self.factors:
                    raise KeyError(f"Factor {name} depends on unknown factor {dep} in procedure {self.name}.")
                in_degree[name] += 1
                dependents[dep].append(name)

        ready = [name for name, degree in in_degree.items() if degree == 0]
        levels = []

        while ready:
            for i in range(0, len(ready), thread_count):
                chunk = ready[i:i + thread_count]
                levels.append([(name, *self.factors[name]) for name in chunk])

            next_ready = []
            for name in ready:
                for dependent in dependents[name]:
                    in_degree[dependent] -= 1
                    if in_degree[dependent] == 0:
                        next_ready.append(dependent)
            ready = next_ready

        if sum(len(level) for level in levels) != len(self.factors):
            raise ValueError(f"Circular dependency detected in procedure {self.name}.")

        return levels


    '''
        Example Usage of topo_sorted_levels:
            from concurrent.futures import ThreadPoolExecutor, wait
            levels = obj.topo_sorted_levels(thread_count=4)
            with ThreadPoolExecutor(max_workers=4) as executor:
                for level in levels:
                    wait([executor.submit(factor.run) for (name, factor, _) in level])
    '''


class AnalysisReport:
    def __init__(self, name='unnamed', procedure=None, framework=None, process=None):
        self.name = name
        self.framework = framework or FRAMEWORKS['default']

        if (not procedure and not process) or (procedure and process):
            raise Exception("Must only define procedure xor process.")
        if procedure:
            self._procedure = self.framework.procedure[procedure]
            self._process = self._procedure.create_process()
            self.results = None
        if process:
            self._procedure = None
            self._process = process
            self.results = self.report()


    def set_input(self, name, inp):
        self._process.set_input(name, inp)
        return self


    def process(self):
        self._process.run()

        self.results = self.report()
        return self


    def report(self):
        return {}


class AnalysisFramework:
    def __init__(self, name='unnamed'):
        self.name = name
        self._formats = {}
        self._factors = {}
        self._procedures = {}
        self._reports = {}


    @property
    def factor(self):
        return self._factors


    @property
    def procedure(self):
        return self._procedures
    

    @property
    def report(self):
        return self._reports


    def _force_register_factor(self, name, factor, config=None):
        if isinstance(factor, tuple):
            from importlib import import_module
            (module_name, class_name) = factor
            factor = getattr(import_module(module_name), class_name)
        else:
            class_name = factor.__name__

        self._factors[name] = type(class_name, (factor,), {'factor_config': config})
        return self._factors[name]


    def register_factor(self, name: str, factor: Union[type, tuple[str, str]], config=None):
        '''
            factor can be a tuple of module_name and class_name (or the object class itself):
                ('thirdparty.yannt.analysis.pparse.plugin', 'PparseFormat')
                PparseFormat
        '''
        if name in self._factors:
            raise Exception(f"Factor {name} is already registered.")

        return self._force_register_factor(name, factor, config=config)


    def _force_register_report(self, name: str, report: Union[type, tuple[str, str]], config=None):
        if isinstance(report, tuple):
            from importlib import import_module
            (module_name, class_name) = report
            report = getattr(import_module(module_name), class_name)
        else:
            class_name = report.__name__

        self._reports[name] = type(class_name, (report,), {'report_config': config})
        return self._reports[name]

    
    def register_report(self, name: str, report: Union[type, tuple[str, str]], config=None):
        '''
            report can be a tuple of module_name and class_name (or the object class itself):
                ('thirdparty.yannt.analysis.pparse.plugin', 'PparseFormat')
                PparseFormat
        '''
        if name in self._reports:
            raise Exception(f"Report {name} is already registered.")

        return self._force_register_report(name, report, config=config)


    def init_report(self, name, procedure):
        if name not in self._reports:
            raise KeyError(f"Report name {name} not registered in framework.")
        return self._reports[name](name=name, procedure=procedure, framework=self)

    
    def post_process_report(self, name, process=None):
        if name not in self._reports:
            raise KeyError(f"Report name {name} not registered in framework.")
        report = self._reports[name](name=name, process=process, framework=self)
        return report


    def create_procedure(self, name='unnamed'):
        if name in self._procedures:
            raise KeyError(f"Procedure name {name} already used in framework.")
        self._procedures[name] = AnalysisProcedure(name=name, framework=self)
        return self._procedures[name]


    # def create_report(self, name='unnamed', procedure=None):
    #     if name in self._reports:
    #         raise KeyError(f"Report name {name} already used in framework.")
    #     self._reports[name] = AnalysisReport(name=name, procedure=procedure, framework=self)
    #     return self._reports[name]


FRAMEWORKS = {'default': AnalysisFramework(name='default')}

