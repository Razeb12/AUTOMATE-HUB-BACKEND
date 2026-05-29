from abc import ABC, abstractmethod
from typing import Optional
from src.sessions.domain.entities import Session

class AbstractSessionRepository(ABC):

    @abstractmethod
    async def get_by_id(self, session_id: str) -> Optional[Session]:
        ...

    @abstractmethod
    async def get_active_by_vehicle(self, vehicle_id: str) -> Optional[Session]:
        ...

    @abstractmethod
    async def save(self, session: Session) -> None:
        ...

    @abstractmethod
    async def list_active(self) -> list[Session]:
        ...
