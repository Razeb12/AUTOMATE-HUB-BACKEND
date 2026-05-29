from datetime import timedelta
from src.auth.infrastructure.jwt_provider import JWTProvider

from src.config import get_settings

class IssueTokenUseCase:
    def __init__(self, provider: JWTProvider):
        self._provider = provider
        self._expected_api_key = get_settings().EXPECTED_API_KEY

    def execute(self, api_key: str) -> str:
        if not api_key or api_key != self._expected_api_key:
            raise ValueError('Invalid API Key provided. Please check your credentials.')
        return self._provider.encode(subject=f'user_{api_key[:8]}', expires_delta=timedelta(hours=24))
