import asyncio
import random
from collections.abc import AsyncGenerator
from src.telemetry.interfaces.abstractions import AbstractOBDSource
from src.telemetry.domain.entities import OBDRawFrame
from src.telemetry.domain.value_objects import PIDCode
from src.telemetry.infrastructure.pid_registry import list_pids
from src.config import get_settings

class OBDSimulator(AbstractOBDSource):

    def __init__(self, poll_interval_ms: int | None=None):
        self._interval = (poll_interval_ms or get_settings().OBD_POLL_INTERVAL_MS) / 1000
        self._state: dict[str, float] = {'010C': 800.0, '010D': 0.0}

    async def stream(self) -> AsyncGenerator[OBDRawFrame, None]:
        while True:
            for pid_code in list_pids():
                frame = self._generate_frame(pid_code)
                if frame:
                    yield frame
            await asyncio.sleep(self._interval)

    def _generate_frame(self, pid_code: str) -> OBDRawFrame | None:
        raw_bytes = self._compute_raw_bytes(pid_code)
        return OBDRawFrame(pid=PIDCode(pid_code), raw_bytes=tuple(raw_bytes))

    def _compute_raw_bytes(self, pid_code: str) -> list[int]:
        match pid_code:
            case '010C':
                self._state['010C'] = max(600, min(7000, self._state['010C'] + random.uniform(-100, 150)))
                enc = int(self._state['010C'] * 4)
                return [enc >> 8, enc & 255]
            case '010D':
                self._state['010D'] = max(0, min(200, self._state['010D'] + random.uniform(-5, 8)))
                return [int(self._state['010D'])]
            case '0105' | '010F':
                return [random.randint(110, 135)]
            case '0111' | '012F' | '0104':
                return [random.randint(30, 220)]
            case _:
                return [0]