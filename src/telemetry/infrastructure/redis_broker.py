import json
from collections.abc import AsyncGenerator
from src.telemetry.interfaces.abstractions import AbstractTelemetryBroker
from src.telemetry.domain.entities import TelemetryFrame
from src.telemetry.domain.value_objects import SessionId
from src.infrastructure.redis_client import get_redis

class RedisTelemetryBroker(AbstractTelemetryBroker):

    def _channel_name(self, session_id: SessionId) -> str:
        return f'telemetry:{session_id.value}'

    async def publish(self, session_id: SessionId, frame: TelemetryFrame) -> None:
        redis = await get_redis()
        payload = json.dumps(frame.to_json_dict())
        await redis.publish(self._channel_name(session_id), payload)

    async def subscribe(self, session_id: SessionId) -> AsyncGenerator[TelemetryFrame, None]:
        redis = await get_redis()
        pubsub = redis.pubsub()
        await pubsub.subscribe(self._channel_name(session_id))
        async for message in pubsub.listen():
            if message['type'] == 'message':
                yield self._deserialise(message['data'])

    def _deserialise(self, data: bytes) -> TelemetryFrame:
        from src.telemetry.domain.value_objects import PIDCode, TelemetryValue
        payload = json.loads(data)
        return TelemetryFrame(session_id=SessionId(payload['session_id']), pid=PIDCode(payload['pid']), label=payload['label'], value=TelemetryValue(raw=payload['value'], unit=payload['unit']))