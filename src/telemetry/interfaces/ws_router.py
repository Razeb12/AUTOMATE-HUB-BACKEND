from fastapi import APIRouter, WebSocket, Depends
from src.telemetry.application.stream_telemetry import StreamTelemetryUseCase
from src.telemetry.domain.value_objects import SessionId
from src.auth.interfaces.ws_auth_dependency import require_ws_token
from src.telemetry.infrastructure.redis_broker import RedisTelemetryBroker
from starlette.websockets import WebSocketDisconnect
router: APIRouter = APIRouter()

def _build_broker():
    return RedisTelemetryBroker()

@router.websocket('/ws/telemetry/{session_id}')
async def telemetry_stream(websocket: WebSocket, session_id: str, _token: str=Depends(require_ws_token)):
    await websocket.accept()
    use_case = StreamTelemetryUseCase(broker=_build_broker())
    try:
        await use_case.run(websocket, SessionId(session_id))
    except WebSocketDisconnect:
        pass