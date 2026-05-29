from fastapi import WebSocket
from src.telemetry.interfaces.abstractions import AbstractTelemetryBroker
from src.telemetry.domain.value_objects import SessionId
import json

class StreamTelemetryUseCase:

    def __init__(self, broker: AbstractTelemetryBroker):
        self._broker = broker

    async def run(self, websocket: WebSocket, session_id: SessionId) -> None:
        async for frame in self._broker.subscribe(session_id):
            await websocket.send_text(json.dumps(frame.to_json_dict()))