"""Dataclasses and YAML loader for analysis framework configuration."""

from dataclasses import dataclass, field
from typing import Optional
import yaml


@dataclass
class FactorClassConfig:
    """Configuration entry for a single factor class.

    Attributes:
        name: Registered name used to look up this factor in a framework.
        module: Dotted module path where the class is defined.
        klass: Class name within the module.
        config: Optional key/value configuration passed to the factor at registration.
    """

    name: str
    module: str
    klass: str
    config: dict = field(default_factory=dict)


@dataclass
class ReportClassConfig:
    """Configuration entry for a single report class.

    Attributes:
        name: Registered name used to look up this report in a framework.
        module: Dotted module path where the class is defined.
        klass: Class name within the module.
        config: Optional key/value configuration passed to the report at registration.
    """

    name: str
    module: str
    klass: str
    config: dict = field(default_factory=dict)


@dataclass
class FactorConfig:
    """Configuration for a worker factor within a procedure.

    Attributes:
        name: Instance name of this factor in the procedure.
        factor_class: Registered factor class name to instantiate.
        dependencies: Names of upstream factors this factor depends on.
    """

    name: str
    factor_class: str
    dependencies: list[str] = field(default_factory=list)


@dataclass
class InputFactorConfig:
    """Configuration for an input factor within a procedure.

    Attributes:
        name: Instance name of this input factor in the procedure.
        factor_class: Registered factor class name to instantiate.
    """

    name: str
    factor_class: str


@dataclass
class ProcedureConfig:
    """Configuration for an analysis procedure (a named factor graph).

    Attributes:
        name: Procedure name.
        input_factors: Ordered list of input factor configurations.
        worker_factors: Ordered list of worker factor configurations.
    """

    name: str
    input_factors: list[InputFactorConfig] = field(default_factory=list)
    worker_factors: list[FactorConfig] = field(default_factory=list)


@dataclass
class FrameworkConfig:
    """Configuration for a single analysis framework.

    Attributes:
        name: Framework name used as the registry key.
        factor_classes: Factor class registrations for this framework.
        report_classes: Report class registrations for this framework.
        procedures: Procedure definitions for this framework.
    """

    name: str
    factor_classes: list[FactorClassConfig] = field(default_factory=list)
    report_classes: list[ReportClassConfig] = field(default_factory=list)
    procedures: list[ProcedureConfig] = field(default_factory=list)


@dataclass
class Config:
    """Top-level configuration object parsed from a YAML config file.

    Attributes:
        frameworks: List of framework configurations to apply.
    """

    frameworks: list[FrameworkConfig] = field(default_factory=list)


def parse_factor_class(data: dict) -> FactorClassConfig:
    """Parse a factor class entry from a raw config dict.

    Args:
        data: Dict with keys `'name'`, `'module'`, `'class'`, and
            optionally `'config'`.

    Returns:
        A :class:`FactorClassConfig` populated from `data`.
    """
    return FactorClassConfig(
        name=data['name'],
        module=data['module'],
        klass=data['class'],
        config=data.get('config', {}),
    )


def parse_report_class(data: dict) -> ReportClassConfig:
    """Parse a report class entry from a raw config dict.

    Args:
        data: Dict with keys `'name'`, `'module'`, `'class'`, and
            optionally `'config'`.

    Returns:
        A :class:`ReportClassConfig` populated from `data`.
    """
    return ReportClassConfig(
        name=data['name'],
        module=data['module'],
        klass=data['class'],
        config=data.get('config', {}),
    )


def parse_procedure(data: dict) -> ProcedureConfig:
    """Parse a procedure entry from a raw config dict.

    Args:
        data: Dict with keys `'name'`, and optionally `'input_factors'`
            and `'worker_factors'`.

    Returns:
        A :class:`ProcedureConfig` populated from `data`.
    """
    return ProcedureConfig(
        name=data['name'],
        input_factors=[
            InputFactorConfig(name=f['factor']['name'], factor_class=f['factor']['factor_class'])
            for f in data.get('input_factors', [])
        ],
        worker_factors=[
            FactorConfig(
                name=f['factor']['name'],
                factor_class=f['factor']['factor_class'],
                dependencies=f['factor'].get('dependencies', []),
            )
            for f in data.get('worker_factors', [])
        ],
    )


def parse_framework(data: dict) -> FrameworkConfig:
    """Parse a framework entry from a raw config dict.

    Args:
        data: Dict with key `'name'` and optional `'factor_classes'`,
            `'report_classes'`, and `'procedures'` lists.

    Returns:
        A :class:`FrameworkConfig` populated from `data`.
    """
    return FrameworkConfig(
        name=data['name'],
        factor_classes=[parse_factor_class(fc['factor_class']) for fc in data.get('factor_classes', [])],
        report_classes=[parse_report_class(rc['report_class']) for rc in data.get('report_classes', [])],
        procedures=[parse_procedure(p['procedure']) for p in data.get('procedures', [])],
    )


def load_config(path: str) -> Config:
    """Load and parse a YAML configuration file.

    Args:
        path: Filesystem path to the YAML config file.

    Returns:
        A :class:`Config` object populated from the file.
    """
    with open(path, 'r') as f:
        raw = yaml.safe_load(f)
    return Config(
        frameworks=[parse_framework(fw['framework']) for fw in raw['config']['frameworks']]
    )