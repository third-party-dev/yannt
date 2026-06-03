#!/usr/bin/env python3


from abc import ABC, abstractmethod
from collections import defaultdict, deque
from typing import Any


AnalysisFactorKey = tuple[type["AnalysisFactor"], str]
AnalysisFactorRegistry = dict[AnalysisFactorKey, "AnalysisFactor"]
class AnalysisFactor():
    def __init__(self, _id = "_init", dependencies = None):
        self._id = _id
        self.dependencies = dependencies or []
        self.result_tags = []
 
    # @property
    # def key(self) -> AnalysisFactorKey:
    #     """``(type(self), self._id)`` — the canonical registry key."""
    #     return (type(self), self._id)
 
    def get_dependencies(self):
        return self.dependencies
 
    # def resolved_dependencies(self) -> list[AnalysisFactorKey]:
    #     """Union of :meth:`dependencies` and any constructor-supplied deps."""
    #     seen: dict[AnalysisFactorKey, None] = {}  # ordered-set via insertion-order dict
    #     for k in self.dependencies():
    #         seen[k] = None
    #     for k in self._extra_dependencies:
    #         seen[k] = None
    #     return list(seen)
 
    def run(self, process):
        print(f"Running in {type(self)}:{self._id}")
        return None
 
    def __repr__(self):
        return f"{type(self).__name__}(_id={self._id!r})"


class AnalysisProcess:

    def __init__(self):
        self.results = {}
        self.registry = {}


    def register_factor(self, factor):
        self.registry[(type(factor), factor._id)] = factor
        return self


    def run(self):
        sorted_factors = self._topological_sort(self.registry)
        for factor_key, factor in sorted_factors:
            self.results[factor_key] = factor.run(self)


    def _topological_sort(self, registry):
        '''
            Example Registry:
                registry = {
                    (TensorsFactor, "_init"): TensorsFactor(_id="_init", dependencies=[(OnnxFormat, "_init")]),
                    (OnnxFormat, "_init"): OnnxFormat(_id="_init"),
                }
            Returns sorted list of items.
        '''

        from collections import defaultdict, deque

        # Verify all dependencies are in registry.
        for key, factor in registry.items():
            for dep_key in factor.get_dependencies():
                if dep_key not in registry:
                    dep_cls, dep_id = dep_key
                    raise KeyError(f"{factor!r} dependency ({dep_cls.__name__!r}, {dep_id!r}) missing from registry.")
    
        # --- Do Adjacency ---
        # Note: When key doesn't exist, auto create set: `dependents[dep_key].add(key)`
        dependents = defaultdict(set)
        in_degree = {key: 0 for key in registry}
    
        for key, factor in registry.items():
            for dep_key in factor.get_dependencies():
                dependents[dep_key].add(key)
                in_degree[key] += 1
    
        # Do topological sort on nodes (Kahn)
        queue: deque[AnalysisFactorKey] = deque(k for k, d in in_degree.items() if d == 0)
        order: list[tuple[AnalysisFactorKey, AnalysisFactor]] = []
    
        while queue:
            key = queue.popleft()
            order.append((key, registry[key]))
            for dependent_key in dependents[key]:
                in_degree[dependent_key] -= 1
                if in_degree[dependent_key] == 0:
                    queue.append(dependent_key)
    
        if len(order) != len(registry):
            cycle_keys = [k for k, d in in_degree.items() if d > 0]
            raise RuntimeError(f"Cycle detected. Nodes blocked: {cycle_keys}")
    
        return order


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