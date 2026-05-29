from src.shared.base_exception import AppError

class InvalidTokenError(AppError):
    def __init__(self, message: str = "Invalid or expired token"):
        super().__init__(message, "INVALID_TOKEN")

class ExpiredTokenError(InvalidTokenError):
    def __init__(self):
        super().__init__("Token has expired")

class UnauthorizedError(AppError):
    def __init__(self):
        super().__init__("Unauthorized", "UNAUTHORIZED")
