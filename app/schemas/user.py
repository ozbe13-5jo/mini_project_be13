from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# --- User Signup ---

# 요청 데이터 스펙 (Request Body)
class UserSignupRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    nickname: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None


# 응답 데이터 스펙 (Response Body)s
class UserSignupResponse(BaseModel):
    username: str
    id: int
    email: EmailStr
    nickname: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    created_at: datetime


class UserResponse(BaseModel):
    id: int
    username: Optional[str]
    email : EmailStr
    nickname : Optional[str]
    created_at : datetime

    model_config = {"from_attributes": True}

class TokenPair(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None

# 예시 API 엔드포인트 스펙 설명
"""
POST /api/users/signup
Request Body: UserSignupRequest
Response Body: UserSignupResponse
Status Code: 201 Created
"""

class UserPostCreate(BaseModel):
    username: str

class UserPostLogin(BaseModel):
    username: str
    password: str

class UserPostResponse(BaseModel):
    id: int
    username: str
    created_at: datetime

    class Config:
        from_attributes = True