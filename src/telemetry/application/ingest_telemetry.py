from src.telemetry.interfaces.abstractions import AbstractOBDSource, AbstractOBDParser, AbstractTelemetryBroker
from src.telemetry.domain.value_objects import SessionId

class IngestTelemetryUseCase:

    def __init__(self, source: AbstractOBDSource, parser: AbstractOBDParser, broker: AbstractTelemetryBroker, session_id: SessionId):
        self._source = source
        self._parser = parser
        self._broker = broker
        self._session_id = session_id

    async def run(self) -> None:
        async for raw_frame in self._source.stream():
            telemetry_frame = self._parser.parse(raw_frame, self._session_id)
            await self._broker.publish(self._session_id, telemetry_frame)