from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from src.telemetry.domain.entities import OBDRawFrame, TelemetryFrame
from src.telemetry.domain.value_objects import SessionId

class AbstractOBDSource(ABC):

    @abstractmethod
    def stream(self) -> AsyncGenerator[OBDRawFrame, None]:
        ...

class AbstractOBDParser(ABC):

    @abstractmethod
    def parse(self, frame: OBDRawFrame, session_id: SessionId) -> TelemetryFrame:
        ...

class AbstractTelemetryBroker(ABC):

    @abstractmethod
    async def publish(self, session_id: SessionId, frame: TelemetryFrame) -> None:
        ...

    @abstractmethod
    def subscribe(self, session_id: SessionId) -> AsyncGenerator[TelemetryFrame, None]:
        ...