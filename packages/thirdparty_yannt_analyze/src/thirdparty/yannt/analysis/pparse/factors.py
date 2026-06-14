"""Placeholder analysis factors for tensor and graph extraction from pparse viewer objects."""

from thirdparty.yannt.analysis.lib import AnalysisFactor

# ! May be useless to have TensorsFactor if it only pulls from Tensor object in pparse viewer object. !
# TODO: Remove tensors from config.yaml and perform metrics on tensors in TensorsMetricsFactor


class TensorsFactor(AnalysisFactor):
    """Analysis factor that extracts tensor data from an upstream pparse viewer result."""

    def __init__(self, name: str = "_init", dependencies: list = []) -> None:
        """Initialize TensorsFactor.

        Args:
            name: Factor instance name.
            dependencies: List of upstream factor names this factor depends on.
        """
        # Setup base class
        super().__init__(name=name, dependencies=dependencies)
        # Grab config from enclosed class object
        self.factor_config = self.__class__.factor_config
        #breakpoint()


    def run(self) -> None:
        """Execute tensor extraction (not yet implemented).

        TODO: Assuming we have a standard pparse view object in dependencies.
        """
        print(f"Running in {type(self)}:{self.name}")
        print(f"  Dependencies: {self.dependencies}")

        # TODO: Assuming we have a standard pparse view object in dependencies.
        breakpoint()

class GraphFactor(AnalysisFactor):
    """Analysis factor that extracts graph data from an upstream pparse viewer result."""

    def __init__(self, name: str = "_init", dependencies: list = []) -> None:
        """Initialize GraphFactor.

        Args:
            name: Factor instance name.
            dependencies: List of upstream factor names this factor depends on.
        """
        # Setup base class
        super().__init__(name=name, dependencies=dependencies)
        # Grab config from enclosed class object
        self.factor_config = self.__class__.factor_config
        #breakpoint()


    def run(self) -> None:
        """Execute graph extraction (not yet implemented).

        TODO: Assuming we have a standard pparse view object in dependencies.
        """
        print(f"Running in {type(self)}:{self.name}")
        print(f"  Dependencies: {self.dependencies}")

        # TODO: Assuming we have a standard pparse view object in dependencies.
        breakpoint()


