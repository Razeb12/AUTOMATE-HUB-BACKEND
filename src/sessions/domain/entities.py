from dataclasses import dataclass, field
from datetime import datetime, UTC
from enum import Enum

class SessionStatus(Enum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"

@dataclass(frozen=True)
class Session:
    id: str
    vehicle_id: str
    status: SessionStatus = SessionStatus.ACTIVE
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_json_dict(self) -> dict:
        return {
            "id": self.id,
            "vehicle_id": self.vehicle_id,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
        }
