from src.shared.base_exception import AppError

class SessionNotFoundError(AppError):
    def __init__(self, session_id: str):
        super().__init__(f"Session '{session_id}' not found", "SESSION_NOT_FOUND")

class SessionAlreadyActiveError(AppError):
    def __init__(self, vehicle_id: str):
        super().__init__(f"Vehicle '{vehicle_id}' already has an active session", "SESSION_ALREADY_ACTIVE")
