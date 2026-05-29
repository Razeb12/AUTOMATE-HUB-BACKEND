import json
from typing import Optional
from datetime import datetime
from src.infrastructure.redis_client import get_redis
from src.sessions.interfaces.abstractions import AbstractSessionRepository
from src.sessions.domain.entities import Session, SessionStatus

class RedisSessionRepository(AbstractSessionRepository):

    SESSION_HASH_KEY = "sessions:active"

    async def get_by_id(self, session_id: str) -> Optional[Session]:
        redis = await get_redis()
        data = await redis.hget(self.SESSION_HASH_KEY, session_id)
        if data:
            return self._deserialise(data)
        return None

    async def get_active_by_vehicle(self, vehicle_id: str) -> Optional[Session]:
        sessions = await self.list_active()
        for session in sessions:
            if session.vehicle_id == vehicle_id:
                return session
        return None

    async def save(self, session: Session) -> None:
        redis = await get_redis()
        if session.status == SessionStatus.COMPLETED:
            await redis.hdel(self.SESSION_HASH_KEY, session.id)
        else:
            await redis.hset(self.SESSION_HASH_KEY, session.id, json.dumps(session.to_json_dict()))

    async def list_active(self) -> list[Session]:
        redis = await get_redis()
        all_sessions_data = await redis.hgetall(self.SESSION_HASH_KEY)
        return [self._deserialise(data) for data in all_sessions_data.values()]

    def _deserialise(self, data: bytes | str) -> Session:
        payload = json.loads(data)
        return Session(
            id=payload["id"],
            vehicle_id=payload["vehicle_id"],
            status=SessionStatus(payload["status"]),
            created_at=datetime.fromisoformat(payload["created_at"])
        )
