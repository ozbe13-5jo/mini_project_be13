from fastapi import Depends, HTTPException
from app.models import User

async def get_current_user() -> User:
    """
    JWT 등 인증 로직에서 현재 로그인한 User 반환
    (여기서는 예시로 DB 첫 번째 유저 반환)
    """
    user = await User.first()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user
