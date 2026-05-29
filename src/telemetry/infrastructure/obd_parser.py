from src.telemetry.interfaces.abstractions import AbstractOBDParser
from src.telemetry.domain.entities import OBDRawFrame, TelemetryFrame
from src.telemetry.domain.value_objects import SessionId, TelemetryValue
from src.telemetry.domain.exceptions import MalformedFrameError
from .pid_registry import get_pid

from collections.abc import Callable

class OBDParser(AbstractOBDParser):

    def parse(self, frame: OBDRawFrame, session_id: SessionId) -> TelemetryFrame:
        self._validate_bytes(frame)
        definition = get_pid(frame.pid.value)
        decoded_value = self._apply_formula(definition.formula, list(frame.raw_bytes))
        return TelemetryFrame(session_id=session_id, pid=frame.pid, label=definition.label, value=TelemetryValue(raw=decoded_value, unit=definition.unit))

    def _validate_bytes(self, frame: OBDRawFrame) -> None:
        if not frame.raw_bytes:
            raise MalformedFrameError(f'Empty byte array for PID {frame.pid.value}')

    def _apply_formula(self, formula: Callable[[list[int]], float], raw_bytes: list[int]) -> float:
        try:
            return formula(raw_bytes)
        except (IndexError, ZeroDivisionError) as exc:
            raise MalformedFrameError(f'Formula failed: {exc}') from exc