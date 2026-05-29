import pytest
from typing import Optional
from src.sessions.interfaces.abstractions import AbstractSessionRepository
from src.sessions.domain.entities import Session
from src.sessions.application.create_session import CreateSessionUseCase
from src.sessions.application.list_sessions import ListSessionsUseCase
from src.sessions.domain.exceptions import SessionAlreadyActiveError

class MockSessionRepository(AbstractSessionRepository):
    def __init__(self):
        self.sessions = []
        
    async def get_by_id(self, session_id: str) -> Optional[Session]:
        for s in self.sessions:
            if s.id == session_id:
                return s
        return None
        
    async def get_active_by_vehicle(self, vehicle_id: str) -> Optional[Session]:
        for s in self.sessions:
            if s.vehicle_id == vehicle_id:
                return s
        return None
        
    async def save(self, session: Session) -> None:
        self.sessions.append(session)
        
    async def list_active(self) -> list[Session]:
        return self.sessions

@pytest.mark.asyncio
async def test_create_session():
    repo = MockSessionRepository()
    uc = CreateSessionUseCase(repo)
    
    session = await uc.execute("vehicle-1")
    assert session.vehicle_id == "vehicle-1"
    assert len(repo.sessions) == 1

@pytest.mark.asyncio
async def test_create_duplicate_session():
    repo = MockSessionRepository()
    uc = CreateSessionUseCase(repo)
    
    await uc.execute("vehicle-1")
    
    with pytest.raises(SessionAlreadyActiveError):
        await uc.execute("vehicle-1")

@pytest.mark.asyncio
async def test_list_sessions():
    repo = MockSessionRepository()
    uc = ListSessionsUseCase(repo)
    create_uc = CreateSessionUseCase(repo)
    
    await create_uc.execute("v1")
    await create_uc.execute("v2")
    
    sessions = await uc.execute()
    assert len(sessions) == 2
    assert {"v1", "v2"} == {s.vehicle_id for s in sessions}
