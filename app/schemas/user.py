from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# --- User Signup ---

# 요청 데이터 스펙 (Request Body)
class UserSignupRequest(BaseModel):
    email: EmailStr
    password: str
    nickname: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None


# 응답 데이터 스펙 (Response Body)s
class UserSignupResponse(BaseModel):
    id: int
    email: EmailStr
    nickname: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    created_at: datetime


# 예시 API 엔드포인트 스펙 설명
"""
POST /api/users/signup
Request Body: UserSignupRequest
Response Body: UserSignupResponse
Status Code: 201 Created
"""

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    nickname: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    created_at: datetime

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
