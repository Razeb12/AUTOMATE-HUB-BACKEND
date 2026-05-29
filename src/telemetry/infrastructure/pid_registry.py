from dataclasses import dataclass
from collections.abc import Callable

@dataclass(frozen=True)
class PIDDefinition:
    label: str
    unit: str
    formula: Callable[[list[int]], float]
    min_value: float
    max_value: float
    warn_threshold: float
    critical_threshold: float
PID_REGISTRY: dict[str, PIDDefinition] = {'010C': PIDDefinition(label='Engine RPM', unit='RPM', formula=lambda b: (b[0] * 256 + b[1]) / 4, min_value=0, max_value=8000, warn_threshold=5500, critical_threshold=6500), '010D': PIDDefinition(label='Vehicle Speed', unit='km/h', formula=lambda b: float(b[0]), min_value=0, max_value=260, warn_threshold=100, critical_threshold=130), '0105': PIDDefinition(label='Coolant Temperature', unit='°C', formula=lambda b: b[0] - 40, min_value=-40, max_value=215, warn_threshold=95, critical_threshold=105), '010F': PIDDefinition(label='Intake Air Temperature', unit='°C', formula=lambda b: b[0] - 40, min_value=-40, max_value=215, warn_threshold=60, critical_threshold=80), '0111': PIDDefinition(label='Throttle Position', unit='%', formula=lambda b: b[0] * 100 / 255, min_value=0, max_value=100, warn_threshold=85, critical_threshold=95), '012F': PIDDefinition(label='Fuel Level', unit='%', formula=lambda b: b[0] * 100 / 255, min_value=0, max_value=100, warn_threshold=15, critical_threshold=5), '0104': PIDDefinition(label='Engine Load', unit='%', formula=lambda b: b[0] * 100 / 255, min_value=0, max_value=100, warn_threshold=80, critical_threshold=95)}

def get_pid(code: str) -> PIDDefinition:
    definition = PID_REGISTRY.get(code)
    if definition is None:
        from src.telemetry.domain.exceptions import UnknownPIDError
        raise UnknownPIDError(code)
    return definition

def list_pids() -> list[str]:
    return list(PID_REGISTRY.keys())