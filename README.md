# Automat Backend

This is the Python backend for the Automat OBD telemetry platform. It is built using **FastAPI** and **Redis**, strictly adhering to **Screaming Architecture**, **SOLID**, and **DRY** principles.

## System Requirements
- Python 3.14+ (managed via `uv`)
- Redis 7+

## Architecture & Directory Structure

The repository is organized by business domain (`telemetry`, `auth`, `sessions`) rather than by technical layer (`controllers`, `services`, etc.).

```text
src/
├── main.py                     # Application wiring, Dependency Injection, Lifespan
├── config.py                   # Environment configuration (pydantic-settings)
│
├── telemetry/                  # DOMAIN: Live vehicle data ingestion & streaming
│   ├── domain/                 # Core entities (TelemetryFrame) and value objects
│   ├── application/            # Use cases (IngestTelemetry, StreamTelemetry)
│   ├── infrastructure/         # External concerns (Redis broker, OBD simulators, PID registry)
│   └── interfaces/             # Entrypoints (WebSocket routers)
│
├── auth/                       # DOMAIN: Identity & Access Management
│   ├── domain/                 # Core auth models (TokenClaims)
│   ├── application/            # Use cases (IssueToken, VerifyToken)
│   ├── infrastructure/         # External concerns (JWT python-jose implementation)
│   └── interfaces/             # Entrypoints (HTTP Auth routes, WS Dependencies)
│
├── sessions/                   # DOMAIN: Vehicle session lifecycle (Planned)
│
├── infrastructure/             # SHARED: Cross-domain technical implementations
│   ├── redis_client.py         # Async Redis connection pool
│   └── background_runner.py    # Asyncio task manager for resilient background workers
│
└── shared/                     # SHARED: Domain-agnostic primitives
    ├── base_exception.py       # Domain base exception
    └── result.py               # Functional Result Monad (Ok/Err)
```

## Running Locally

1. **Start Redis**:
   ```bash
   docker-compose up -d
   ```
2. **Install Dependencies & Start**:
   ```bash
   uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## Design Philosophy

- **Single Responsibility (SRP)**: Every class, function, and file does exactly one thing. Example: `OBDParser` only parses frames; it does not read from the network or publish to Redis.
- **Dependency Inversion (DIP)**: High-level use cases depend only on abstractions (`AbstractTelemetryBroker`, `AbstractOBDSource`), making it trivial to swap a real ELM327 interface with our `OBDSimulator`.
- **Open/Closed (OCP)**: The `PID_REGISTRY` is the single source of truth. Adding a new PID requires modifying only the registry dictionary—no changes to the parser, validator, or frontend.
