from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


# --- Auth / Users only (team common excludes non-auth schemas) ---

class UserSignupRequest(BaseModel):
    email: EmailStr
    password: str
    nickname: Optional[str] = None


# UserLoginRequest는 OAuth2PasswordRequestForm을 사용하므로 제거


class TokenPair(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    nickname: Optional[str] = None
    created_at: datetime
