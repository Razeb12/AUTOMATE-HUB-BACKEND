from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List
from src.sessions.application.create_session import CreateSessionUseCase
from src.sessions.application.list_sessions import ListSessionsUseCase
from src.sessions.infrastructure.session_repository import RedisSessionRepository
from src.sessions.domain.exceptions import SessionAlreadyActiveError

router: APIRouter = APIRouter()
repository = RedisSessionRepository()

class CreateSessionRequest(BaseModel):
    vehicle_id: str

class SessionResponse(BaseModel):
    id: str
    vehicle_id: str
    status: str
    created_at: str

@router.post("", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(request: CreateSessionRequest):
    use_case = CreateSessionUseCase(repository=repository)
    try:
        session = await use_case.execute(request.vehicle_id)
        return session.to_json_dict()
    except SessionAlreadyActiveError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.get("", response_model=List[SessionResponse])
async def list_sessions():
    use_case = ListSessionsUseCase(repository=repository)
    sessions = await use_case.execute()
    return [session.to_json_dict() for session in sessions]
