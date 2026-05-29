import pytest
from datetime import datetime, UTC
from unittest.mock import patch, AsyncMock
from src.telemetry.infrastructure.redis_broker import RedisTelemetryBroker
from src.telemetry.domain.entities import TelemetryFrame
from src.telemetry.domain.value_objects import SessionId, PIDCode, TelemetryValue

@pytest.mark.asyncio
async def test_redis_broker_publish():
    broker = RedisTelemetryBroker()
    frame = TelemetryFrame(
        session_id=SessionId("sess-1"),
        pid=PIDCode("010C"),
        label="RPM",
        value=TelemetryValue(1000.0, "RPM"),
        timestamp=datetime.now(UTC)
    )
    
    with patch("src.telemetry.infrastructure.redis_broker.get_redis", new_callable=AsyncMock) as mock_get_redis:
        mock_redis = AsyncMock()
        mock_get_redis.return_value = mock_redis
        
        await broker.publish(SessionId("sess-1"), frame)
        
        mock_redis.publish.assert_called_once()
        args = mock_redis.publish.call_args[0]
        assert args[0] == "telemetry:sess-1"
        assert "1000.0" in args[1]
