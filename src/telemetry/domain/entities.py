from dataclasses import dataclass, field
from datetime import datetime, UTC
from .value_objects import PIDCode, SessionId, TelemetryValue

@dataclass(frozen=True)
class OBDRawFrame:
    pid: PIDCode
    raw_bytes: tuple[int, ...]
    captured_at: datetime = field(default_factory=lambda: datetime.now(UTC))

@dataclass(frozen=True)
class TelemetryFrame:
    session_id: SessionId
    pid: PIDCode
    label: str
    value: TelemetryValue
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_json_dict(self) -> dict:
        return {'session_id': self.session_id.value, 'pid': self.pid.value, 'label': self.label, 'value': self.value.raw, 'unit': self.value.unit, 'timestamp': self.timestamp.isoformat()}