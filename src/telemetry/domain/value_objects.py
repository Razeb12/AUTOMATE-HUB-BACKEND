from dataclasses import dataclass

@dataclass(frozen=True)
class PIDCode:
    value: str

    def __post_init__(self):
        if len(self.value) != 4 or not self.value.isalnum():
            raise ValueError(f'Invalid PID code: {self.value}')

@dataclass(frozen=True)
class SessionId:
    value: str

@dataclass(frozen=True)
class TelemetryValue:
    raw: float
    unit: str

    def formatted(self, precision: int=1) -> str:
        return f'{self.raw:.{precision}f} {self.unit}'