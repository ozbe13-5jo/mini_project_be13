from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from app.models import User
from app.schemas.user import UserPostCreate, UserPostLogin, UserPostResponse
from app.auth.auth import create_access_token  # JWT 생성 함수
from app.models import TokenBlacklist

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# 회원가입
@router.post("/register", response_model=UserPostResponse, status_code=201)
async def register(user: UserPostCreate) -> UserPostResponse:
    exists = await User.filter(username=user.username).first()
    if exists:
        raise HTTPException(status_code=400, detail="Username already registered")

    user_obj = await User.create(
        username=user.username,
        password_hash=get_password_hash(user.password)
    )

    return UserPostResponse(
        id=user_obj.id,
        username=user_obj.username,
        created_at=user_obj.created_at
    )


# 로그인
@router.post("/login")
async def login(user: UserPostLogin):
    user_obj = await User.filter(username=user.username).first()
    if not user_obj or not verify_password(user.password, user_obj.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token({"sub": str(user_obj.id)})
    return {"access_token": access_token, "token_type": "bearer"}


# 로그아웃 (선택, JWT blacklist 사용 시)
@router.post("/logout")
async def logout(token: str = Depends(...)):  # Depends로 OAuth2PasswordBearer 사용 가능
    await TokenBlacklist.get_or_create(token=token)
    return {"message": "Logged out"}
