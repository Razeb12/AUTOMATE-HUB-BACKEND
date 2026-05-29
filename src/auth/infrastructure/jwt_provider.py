from jose import jwt
from datetime import datetime, timedelta, UTC
from src.config import get_settings
from src.auth.domain.entities import TokenClaims
from src.auth.domain.exceptions import InvalidTokenError, ExpiredTokenError

class JWTProvider:
    def __init__(self):
        self._secret = get_settings().SECRET_KEY
        self._algorithm = "HS256"

    def encode(self, subject: str, expires_delta: timedelta) -> str:
        expire = datetime.now(UTC) + expires_delta
        to_encode = {"sub": subject, "exp": int(expire.timestamp())}
        return jwt.encode(to_encode, self._secret, algorithm=self._algorithm)

    def decode(self, token: str) -> TokenClaims:
        try:
            payload = jwt.decode(token, self._secret, algorithms=[self._algorithm])
            sub = payload.get("sub")
            exp = payload.get("exp")
            if sub is None or exp is None:
                raise InvalidTokenError()
            return TokenClaims(sub=sub, exp=exp, raw=payload)
        except jwt.ExpiredSignatureError:
            raise ExpiredTokenError()
        except jwt.JWTError:
            raise InvalidTokenError()
