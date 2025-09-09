from fastapi import APIRouter
from app.schemas.user import UserSignupRequest, UserSignupResponse

router = APIRouter()

@router.post("/signup", response_model=UserSignupResponse, status_code=201)
async def signup(user: UserSignupRequest):
    # 서비스 호출 → DB에 저장
    created_user = await create_user_in_db(user)
    return created_user
