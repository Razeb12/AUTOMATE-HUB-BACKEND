from dataclasses import dataclass

@dataclass(frozen=True)
class TokenClaims:
    sub: str
    exp: int
    raw: dict[str, object]
