from src.auth.infrastructure.jwt_provider import JWTProvider
from src.auth.domain.entities import TokenClaims

class VerifyTokenUseCase:
    def __init__(self, provider: JWTProvider):
        self._provider = provider

    def execute(self, raw_token: str) -> TokenClaims:
        return self._provider.decode(raw_token)
