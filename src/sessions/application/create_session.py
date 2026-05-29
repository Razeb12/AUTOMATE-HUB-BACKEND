import uuid
from src.sessions.interfaces.abstractions import AbstractSessionRepository
from src.sessions.domain.entities import Session
from src.sessions.domain.exceptions import SessionAlreadyActiveError

class CreateSessionUseCase:

    def __init__(self, repository: AbstractSessionRepository):
        self._repository = repository

    async def execute(self, vehicle_id: str) -> Session:
        existing = await self._repository.get_active_by_vehicle(vehicle_id)
        if existing:
            raise SessionAlreadyActiveError(vehicle_id)

        session = Session(id=str(uuid.uuid4()), vehicle_id=vehicle_id)
        await self._repository.save(session)
        return session
