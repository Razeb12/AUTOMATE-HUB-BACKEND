import pytest
from src.telemetry.infrastructure.obd_simulator import OBDSimulator

@pytest.mark.asyncio
async def test_obd_simulator_yields_frames():
    simulator = OBDSimulator(poll_interval_ms=10)
    frames = []
    
    async for frame in simulator.stream():
        frames.append(frame)
        if len(frames) >= 3:
            break
            
    assert len(frames) == 3
    for frame in frames:
        assert frame.pid.value is not None
        assert isinstance(frame.raw_bytes, tuple)
