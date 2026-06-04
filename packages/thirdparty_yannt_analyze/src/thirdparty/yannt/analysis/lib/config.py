from dataclasses import dataclass, field
from typing import Optional
import yaml


@dataclass
class FactorClassConfig:
    name: str
    module: str
    klass: str
    config: dict = field(default_factory=dict)


@dataclass
class ReportClassConfig:
    name: str
    module: str
    klass: str
    config: dict = field(default_factory=dict)


@dataclass
class FactorConfig:
    name: str
    factor_class: str
    dependencies: list[str] = field(default_factory=list)


@dataclass
class InputFactorConfig:
    name: str
    factor_class: str


@dataclass
class ProcedureConfig:
    name: str
    input_factors: list[InputFactorConfig] = field(default_factory=list)
    worker_factors: list[FactorConfig] = field(default_factory=list)


@dataclass
class FrameworkConfig:
    name: str
    factor_classes: list[FactorClassConfig] = field(default_factory=list)
    report_classes: list[ReportClassConfig] = field(default_factory=list)
    procedures: list[ProcedureConfig] = field(default_factory=list)


@dataclass
class Config:
    frameworks: list[FrameworkConfig] = field(default_factory=list)


def parse_factor_class(data: dict) -> FactorClassConfig:
    return FactorClassConfig(
        name=data['name'],
        module=data['module'],
        klass=data['class'],
        config=data.get('config', {}),
    )


def parse_report_class(data: dict) -> ReportClassConfig:
    return ReportClassConfig(
        name=data['name'],
        module=data['module'],
        klass=data['class'],
        config=data.get('config', {}),
    )


def parse_procedure(data: dict) -> ProcedureConfig:
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
    return FrameworkConfig(
        name=data['name'],
        factor_classes=[parse_factor_class(fc['factor_class']) for fc in data.get('factor_classes', [])],
        report_classes=[parse_report_class(rc['report_class']) for rc in data.get('report_classes', [])],
        procedures=[parse_procedure(p['procedure']) for p in data.get('procedures', [])],
    )


def load_config(path: str) -> Config:
    with open(path, 'r') as f:
        raw = yaml.safe_load(f)
    return Config(
        frameworks=[parse_framework(fw['framework']) for fw in raw['config']['frameworks']]
    )