from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# --- User Signup ---
class UserBase(BaseModel):
    username: Optional[str] =None
    email: Optional[EmailStr] =None
    name: Optional[str] =None

# 요청 데이터 스펙 (Request Body)
class UserSignupRequest(UserBase):
    password: str

# 응답 데이터 스펙 (Response Body)s
class UserSignupResponse(UserBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}

class UserResponse(UserBase):
    id: int
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

class UserPostCreate(UserBase):
    username: str

class UserPostLogin(BaseModel):
    username: str
    password: str

class UserPostResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True