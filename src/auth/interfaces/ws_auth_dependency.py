from fastapi import Query, WebSocket
from src.auth.application.verify_token import VerifyTokenUseCase
from src.auth.domain.exceptions import InvalidTokenError
from src.auth.infrastructure.jwt_provider import JWTProvider

async def require_ws_token(
    websocket: WebSocket,
    token: str = Query(...)
) -> str:
    try:
        use_case = VerifyTokenUseCase(provider=JWTProvider())
        use_case.execute(token)
        return token
    except InvalidTokenError:
        await websocket.close(code=4001)
        raise
