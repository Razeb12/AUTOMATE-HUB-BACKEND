from src.shared.base_exception import AppError

class UnknownPIDError(AppError):

    def __init__(self, code: str):
        super().__init__(f'Unknown PID code: {code}', 'UNKNOWN_PID')

class MalformedFrameError(AppError):

    def __init__(self, message: str):
        super().__init__(f'Malformed frame: {message}', 'MALFORMED_FRAME')