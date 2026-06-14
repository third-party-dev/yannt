#!/usr/bin/env python3
"""Core analysis framework: factor graph execution, procedures, and report generation."""


from abc import ABC, abstractmethod
from collections import defaultdict, deque
from typing import Any, Union, Optional


AnalysisFactorKey = tuple[type["AnalysisFactor"], str]
AnalysisFactorRegistry = dict[AnalysisFactorKey, "AnalysisFactor"]
class AnalysisFactor():
    """Base class for all analysis factors in a procedure.

    A factor encapsulates a single unit of computation within an
    ``AnalysisProcess``.  Subclasses override `run` to produce a
    result that is stored in the process result dict under the factor's name.

    Attributes:
        name: Instance name assigned at procedure build time.
        dependencies: Names of upstream factors whose results this factor may
            read via `get_result`.
        result_tags: Arbitrary tags for categorizing result entries.
    """
    def __init__(self, name: str = 'unnamed', dependencies: Optional[list] = None) -> None:
        """Initialize an AnalysisFactor.

        Args:
            name: (Printable) Name for this factor instance.
            dependencies: Names of upstream factors whose results are needed.
        """
        # The name of the factor
        self.name = name

        # Note: These dependencies are for reference only, not for sorting.
        self.dependencies = dependencies or []

        self.result_tags = []


    def get_name(self) -> str:
        """Return the factor's instance name.

        Returns:
            The name assigned at initialization.
        """
        return self.name


    def get_results(self) -> dict:
        """Return the full results dictionary for the process.

        Returns:
            The `AnalysisProcess.results` mapping.
        """
        return self._process.results


    def get_result(self, name: str) -> Any:
        """Return the single result for `name` factor.

        Args:
            name: Key of the result to retrieve.

        Returns:
            The stored result value for `name`.
        """
        return self.get_results()[name]


    def run(self) -> None:
        """Execute the factor's DAG/network/graph.

        Subclasses override this method to produce a result.  The return value
        is stored in the process result dictionary under this factor's name.
        """
        pass
        # #from pprint import pprint
        # print(f"Running in {type(self)}:{self.name} with result:")
        # #pprint(dict(process.results))
        # return None


    def __repr__(self) -> str:
        """Return a debug-friendly representation of the factor.

        Returns:
            String in the form `ClassName(name='...')`.
        """
        return f"{type(self).__name__}(name={self.name!r})"


class AnalysisInput(AnalysisFactor):
    """An ``AnalysisFactor`` that holds an external input value.

    Input factors occupy the leaf positions in a procedure's factor graph.
    Their `input` must be set via `set_input` before the process
    is run.
    """

    def __init__(self, name: str = 'unnamed', dependencies: Optional[list] = None) -> None:
        """Initialize an AnalysisInput.

        Args:
            name: Human-readable name for this input factor instance.
            dependencies: Names of upstream factors (usually empty for inputs).
        """
        super().__init__(name=name, dependencies=dependencies)
        self.input = None


    def get_input(self) -> Any:
        """Return the raw input value.

        Returns:
            The value previously set via `set_input`, or `None`.
        """
        return self.input


    def missing_input(self) -> bool:
        """Check whether the input value has not been set.

        Returns:
            True if `input` is `None`.
        """
        return self.input is None


    def set_input(self, inp: Any) -> 'AnalysisInput':
        """Set the input value for this factor.

        Args:
            inp: The input value to store.

        Returns:
            `self`, for method chaining.
        """
        self.input = inp
        return self


class AnalysisProcess:
    """Executes an ordered list of ``AnalysisFactor`` instances and collects results.

    An ``AnalysisProcess`` is instantiated by `AnalysisProcedure.create_process`
    with a topologically-sorted list of factor objects.  Call `set_input` for every
    input factor, then `run` to execute the graph.
    """

    def __init__(self, factor_obj_list: list) -> None:
        """Initialize an AnalysisProcess.

        Args:
            factor_obj_list: Topologically-sorted list of ``AnalysisFactor`` instances to execute.
        """
        self.factor_obj_list = factor_obj_list
        self.factors_objs = defaultdict(dict)
        self.results = defaultdict(dict)
        self.input_factors = {}

        for factor_obj in self.factor_obj_list:
            if isinstance(factor_obj, AnalysisInput):
                self.input_factors[factor_obj.name] = factor_obj
            factor_obj._process = self


    def set_input(self, name: str, inp: Any) -> 'AnalysisProcess':
        """Assign an input value to a named input factor.

        Args:
            name: Name of the input factor to assign.
            inp: Value to pass to that input factor.

        Returns:
            `self`, for method chaining.
        """
        self.input_factors[name].set_input(inp)
        return self


    def run(self) -> 'AnalysisProcess':
        """Execute the factor graph in order.

        Returns:
            `self`, for method chaining.

        Raises:
            Exception: If any input factor has not been assigned a value.
        """
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
    """A named, reusable factor graph definition within a framework.

    A procedure declares which factor classes to use (inputs and workers) and
    their dependency relationships.  Call `create_process` to build a
    runnable ``AnalysisProcess`` from the procedure.
    """

    def __init__(self, name: str = 'unnamed', framework: Optional['AnalysisFramework'] = None) -> None:
        """Initialize an AnalysisProcedure.

        Args:
            name: Procedure name; must be unique within its framework.
            framework: The owning ``AnalysisFramework``.  Defaults to the
                global `FRAMEWORKS['default']` instance.
        """
        self.name = name

        self.framework = framework
        if self.framework is None:
            self.framework = FRAMEWORKS['default']

        self.inputs = {}
        self.factors = {}


    def _force_add_input(self, name: str, factor: str) -> 'AnalysisProcedure':
        """Add or overwrite an input factor in the procedure.

        Args:
            name: Instance name for the input in this procedure.
            factor: Registered factor class name to use as the input.

        Returns:
            `self`, for method chaining.

        Raises:
            KeyError: If `factor` is not registered in the framework.
        """
        if factor not in self.framework.factor:
            raise KeyError(f"Factor {factor} not registered in framework {self.framework.name}.")
        self.inputs[name] = self.framework.factor[factor]
        self._force_add_factor(name, factor)
        return self


    def add_input(self, name: str, factor: str) -> 'AnalysisProcedure':
        """Add an input factor to the procedure, raising on duplicate names.

        Args:
            name: Instance name for the input in this procedure.
            factor: Registered factor class name to use as the input.

        Returns:
            `self`, for method chaining.

        Raises:
            KeyError: If `factor` is not registered in the framework.
            ValueError: If `name` is already used in this procedure.
        """
        if factor not in self.framework.factor:
            raise KeyError(f"Factor {factor} not registered in framework {self.framework.name}.")
        if name in self.inputs:
            raise ValueError(f"Duplicate input name {name} added to process {self.name}.")
        self.inputs[name] = self.framework.factor[factor]
        self.add_factor(name, factor)
        return self


    def _force_add_factor(self, name: str, factor: str, dependencies: Optional[list] = None) -> 'AnalysisProcedure':
        """Add or overwrite a worker factor in the procedure.

        Args:
            name: Instance name for the factor in this procedure.
            factor: Registered factor class name.
            dependencies: Names of upstream factors this factor depends on.

        Returns:
            `self`, for method chaining.

        Raises:
            KeyError: If ``factor`` is not registered in the framework.
        """
        if factor not in self.framework.factor:
            raise KeyError(f"Factor {factor} not registered in framework {self.framework.name}.")
        self.factors[name] = (self.framework.factor[factor], dependencies or [])
        return self


    def add_factor(self, name: str, factor: str, dependencies: Optional[list] = None) -> 'AnalysisProcedure':
        """Add a worker factor to the procedure, raising on duplicate names.

        Args:
            name: Instance name for the factor in this procedure.
            factor: Registered factor class name.
            dependencies: Names of upstream factors this factor depends on.

        Returns:
            `self`, for method chaining.

        Raises:
            ValueError: If `name` is already used in this procedure.
        """
        if name in self.factors:
            raise ValueError(f"Duplicate factor name {name} added to process {self.name}.")
        self._force_add_factor(name, factor, dependencies=dependencies)
        return self


    def create_process(self) -> AnalysisProcess:
        """Instantiate all factors and return a runnable AnalysisProcess.

        Factors are instantiated in topological order so each worker can read
        results from its declared dependencies.

        Returns:
            A new ``AnalysisProcess`` ready to receive inputs and be run.
        """
        factor_objs = []
        factor_cls_list = self.topo_sorted_factors()
        for factor_name, factor_cls, factor_deps in factor_cls_list:
            factor_obj = factor_cls(name=factor_name, dependencies=factor_deps)
            factor_objs.append(factor_obj)
        
        return AnalysisProcess(factor_objs)


    def topo_sorted_factors(self) -> list[tuple]:
        """Return factors in topological (dependency) order.

        Returns:
            A list of `(name, factor_cls, dependencies)` tuples sorted so
            that every factor appears after all its declared dependencies.

        Raises:
            ValueError: If a circular dependency is detected.
            KeyError: If a dependency name is not present in the procedure.
        """
        visited = set()
        visiting = set()
        result = []

        def visit(name: str) -> None:
            """Recursively visit a factor and its dependencies (DFS).

            Args:
                name: Factor name to visit.

            Raises:
                ValueError: If a back-edge (cycle) is detected.
                KeyError: If `name` depends on an unknown factor.
            """
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
    

    def topo_sorted_levels(self, thread_count: int) -> list[list[tuple]]:
        """Group factors into parallel execution levels for multi-threaded use.

        Uses a BFS-based topological sort that batches independent factors into
        chunks of at most `thread_count` entries per level.

        Args:
            thread_count: Maximum number of factors to include in a single level
                chunk (i.e. the thread pool width).

        Returns:
            A list of levels, where each level is a list of
            `(name, factor_cls, dependencies)` tuples that can be executed
            concurrently.

        Raises:
            KeyError: If any factor depends on an unknown factor.
            ValueError: If a circular dependency is detected.
        """
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
    """Base class for post-process reporting on a completed or new analysis process.

    Either `procedure` (to run a new process) or `process` (to wrap an
    already-executed one) must be provided — not both.  Subclasses override
    `report` to extract and format results.
    """

    def __init__(self, name: str = 'unnamed', procedure: Optional[str] = None, framework: Optional['AnalysisFramework'] = None, process: Optional[AnalysisProcess] = None) -> None:
        """Initialize an AnalysisReport.

        Args:
            name: Report name.
            procedure: Name of a registered procedure to create a new process from.
            framework: The owning ``AnalysisFramework``.  Defaults to
                `FRAMEWORKS['default']`.
            process: A pre-existing ``AnalysisProcess`` to report on.

        Raises:
            Exception: If both or neither of `procedure` and `process` are given.
        """
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


    def set_input(self, name: str, inp: Any) -> 'AnalysisReport':
        """Assign an input value to the underlying process.

        Args:
            name: Input factor name to assign.
            inp: Value to pass to that input factor.

        Returns:
            `self`, for method chaining.
        """
        self._process.set_input(name, inp)
        return self


    def process(self) -> 'AnalysisReport':
        """Run the underlying process and populate :attr:`results`.

        Returns:
            `self`, for method chaining.
        """
        self._process.run()

        self.results = self.report()
        return self


    def report(self) -> dict:
        """Generate the report dict from the completed process results.

        Subclasses override this method to extract and format relevant results.

        Returns:
            A dict of report outputs.  The base implementation returns `{}`.
        """
        return {}


class AnalysisFramework:
    """Top-level container for factor classes, report classes, and procedures.

    A framework acts as a named registry that ties together factor and report
    class definitions with the procedures that use them.  The global
    `FRAMEWORKS` dict holds the default instance and any additional
    frameworks registered by plugins.
    """

    def __init__(self, name: str = 'unnamed') -> None:
        """Initialize an AnalysisFramework.

        Args:
            name: Human-readable name for this framework instance.
        """
        self.name = name
        self._formats = {}
        self._factors = {}
        self._procedures = {}
        self._reports = {}


    @property
    def factor(self) -> dict[str, type]:
        """Return the registered factor class dict.

        Returns:
            Mapping of factor name to dynamically-created factor class.
        """
        return self._factors


    @property
    def procedure(self) -> dict[str, 'AnalysisProcedure']:
        """Return the registered procedure dict.

        Returns:
            Mapping of procedure name to ``AnalysisProcedure`` instance.
        """
        return self._procedures


    @property
    def report(self) -> dict[str, type]:
        """Return the registered report class dict.

        Returns:
            Mapping of report name to dynamically-created report class.
        """
        return self._reports


    def _force_register_factor(self, name: str, factor: Union[type, tuple[str, str]], config: Optional[dict] = None) -> type:
        """Register or overwrite a factor class, closing it over `config`.

        Args:
            name: Registry key for this factor.
            factor: Either a class object or a `(module, classname)` tuple
                that will be imported at registration time.
            config: Optional configuration dict stored as a `factor_config`
                class attribute on the registered class.

        Returns:
            The dynamically-created subclass stored in the factor registry.
        """
        if isinstance(factor, tuple):
            from importlib import import_module
            (module_name, class_name) = factor
            factor = getattr(import_module(module_name), class_name)
        else:
            class_name = factor.__name__

        self._factors[name] = type(class_name, (factor,), {'factor_config': config})
        return self._factors[name]


    def register_factor(self, name: str, factor: Union[type, tuple[str, str]], config: Optional[dict] = None) -> type:
        """Register a factor class, raising if the name is already taken.

        Use this when first-time registration is expected and silent overwrites
        would be a bug.  Use `_force_register_factor` when you intentionally
        want to overwrite an existing entry (e.g. from a config file or CLI).

        Args:
            name: Registry key for this factor.
            factor: Either a class object or a `(module, classname)` tuple
                that will be imported at registration time, e.g.
                `('thirdparty.yannt.analysis.pparse.plugin', 'PparseFormat')`.
            config: Optional configuration dict stored as a `factor_config`
                class attribute on the registered class.

        Returns:
            The dynamically-created subclass stored in the factor registry.

        Raises:
            Exception: If `name` is already registered in this framework.
        """

        '''
            factor can be a tuple of module_name and class_name (or the object class itself):
                ('thirdparty.yannt.analysis.pparse.plugin', 'PparseFormat')
                PparseFormat
        '''
        if name in self._factors:
            raise Exception(f"Factor {name} is already registered.")

        return self._force_register_factor(name, factor, config=config)


    def _force_register_report(self, name: str, report: Union[type, tuple[str, str]], config: Optional[dict] = None) -> type:
        """Register or overwrite a report class, closing it over `config`.

        Args:
            name: Registry key for this report.
            report: Either a class object or a `(module, classname)` tuple
                that will be imported at registration time.
            config: Optional configuration dict stored as a `report_config`
                class attribute on the registered class.

        Returns:
            The dynamically-created subclass stored in the report registry.
        """
        if isinstance(report, tuple):
            from importlib import import_module
            (module_name, class_name) = report
            report = getattr(import_module(module_name), class_name)
        else:
            class_name = report.__name__

        self._reports[name] = type(class_name, (report,), {'report_config': config})
        return self._reports[name]

    
    def register_report(self, name: str, report: Union[type, tuple[str, str]], config: Optional[dict] = None) -> type:
        """Register a report class, raising if the name is already taken.

        Use this when first-time registration is expected and silent overwrites
        would be a bug.  Use `_force_register_report` when you intentionally
        want to overwrite an existing entry (e.g. from a config file or CLI).

        Args:
            name: Registry key for this report.
            report: Either a class object or a `(module, classname)` tuple
                that will be imported at registration time, e.g.
                `('thirdparty.yannt.analysis.pparse.plugin', 'FineTunedReport')`.
            config: Optional configuration dict stored as a `report_config`
                class attribute on the registered class.

        Returns:
            The dynamically-created subclass stored in the report registry.

        Raises:
            Exception: If `name` is already registered in this framework.
        """

        '''
            report can be a tuple of module_name and class_name (or the object class itself):
                ('thirdparty.yannt.analysis.pparse.plugin', 'PparseFormat')
                PparseFormat
        '''
        if name in self._reports:
            raise Exception(f"Report {name} is already registered.")

        return self._force_register_report(name, report, config=config)


    def init_report(self, name: str, procedure: str) -> AnalysisReport:
        """Create a report instance backed by a newly-created process.

        Args:
            name: Registered report class name.
            procedure: Registered procedure name used to create the process.

        Returns:
            An ``AnalysisReport`` instance ready for input assignment and
            `~AnalysisReport.process` execution.

        Raises:
            KeyError: If `name` is not a registered report class.
        """
        if name not in self._reports:
            raise KeyError(f"Report name {name} not registered in framework.")
        return self._reports[name](name=name, procedure=procedure, framework=self)


    def post_process_report(self, name: str, process: Optional[AnalysisProcess] = None) -> AnalysisReport:
        """Create a report instance wrapping an already-completed process.

        Args:
            name: Registered report class name.
            process: An already-executed ``AnalysisProcess`` whose
                results will be passed to the report.

        Returns:
            An ``AnalysisReport`` instance with `~AnalysisReport.results`
            already populated.

        Raises:
            KeyError: If `name` is not a registered report class.
        """
        if name not in self._reports:
            raise KeyError(f"Report name {name} not registered in framework.")
        report = self._reports[name](name=name, process=process, framework=self)
        return report


    def create_procedure(self, name: str = 'unnamed') -> AnalysisProcedure:
        """Create and register a new procedure in this framework.

        Args:
            name: Unique procedure name.

        Returns:
            The newly-created ``AnalysisProcedure`` instance.

        Raises:
            KeyError: If `name` is already used by an existing procedure.
        """
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

