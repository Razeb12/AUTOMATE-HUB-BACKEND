from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.infrastructure.redis_client import init_redis, close_redis
from src.infrastructure.background_runner import BackgroundRunner
from src.telemetry.interfaces.ws_router import router as telemetry_ws_router
from src.telemetry.application.ingest_telemetry import IngestTelemetryUseCase
from src.telemetry.infrastructure.obd_simulator import OBDSimulator
from src.telemetry.infrastructure.obd_parser import OBDParser
from src.telemetry.infrastructure.redis_broker import RedisTelemetryBroker
from src.telemetry.domain.value_objects import SessionId
from src.auth.interfaces.http_router import router as auth_router
from src.sessions.interfaces.http_router import router as sessions_router
from src.config import get_settings

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_redis()
    runner = BackgroundRunner()
    
    use_case = IngestTelemetryUseCase(
        source=OBDSimulator(),
        parser=OBDParser(),
        broker=RedisTelemetryBroker(),
        session_id=SessionId("test-session")
    )
    
    await runner.start(use_case.run)
    yield
    await runner.stop()
    await close_redis()

app = FastAPI(title="Automat OBD Platform", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.CORS_ORIGINS, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(auth_router, prefix="/auth")
app.include_router(sessions_router, prefix="/sessions")
app.include_router(telemetry_ws_router)