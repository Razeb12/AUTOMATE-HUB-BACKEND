from src.sessions.interfaces.abstractions import AbstractSessionRepository
from src.sessions.domain.entities import Session

class ListSessionsUseCase:

    def __init__(self, repository: AbstractSessionRepository):
        self._repository = repository

    async def execute(self) -> list[Session]:
        return await self._repository.list_active()
