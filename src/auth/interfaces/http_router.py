from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel
from src.auth.application.issue_token import IssueTokenUseCase
from src.auth.infrastructure.jwt_provider import JWTProvider

router = APIRouter()
provider = JWTProvider()

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'

@router.post('/token', response_model=TokenResponse)
async def login(x_api_key: str = Header(...)):
    try:
        use_case = IssueTokenUseCase(provider=provider)
        token = use_case.execute(x_api_key)
        return TokenResponse(access_token=token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e), headers={'WWW-Authenticate': 'Bearer'})
