from datetime import datetime, timedelta, timezone
import os
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.db import init_tortoise
from app.models import User, TokenBlacklist
from app.schemas import UserSignupRequest, UserResponse, TokenPair


# app = FastAPI(title="Diary Project")  # Moved below with lifespan


# --------------------
# Settings / Security
# --------------------
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")


def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    # Check blacklist first
    black = await TokenBlacklist.filter(token=token).first()
    if black is not None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token revoked")

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await User.filter(id=int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user


from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_tortoise(app, db_url=os.getenv("DB_URL", "sqlite://db.sqlite3"))
    yield
    # Shutdown
    pass

app = FastAPI(title="Diary Project", lifespan=lifespan)


# Note: Only common + auth endpoints are included.


# --------------------
# Auth / Users
# --------------------


@app.post("/api/users/signup", response_model=UserResponse, status_code=201)
async def signup(payload: UserSignupRequest) -> UserResponse:
    exists = await User.filter(email=str(payload.email)).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = await User.create(
        email=str(payload.email),
        password_hash=get_password_hash(payload.password),
        nickname=payload.nickname,
    )
    return UserResponse(
        id=user.id,
        email=user.email,
        nickname=user.nickname,
        created_at=user.created_at,
    )


@app.post("/api/users/login", response_model=TokenPair)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> TokenPair:
    user = await User.filter(email=form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = create_access_token({"sub": str(user.id)})
    return TokenPair(access_token=token)


@app.post("/api/users/logout")
async def logout(token: str = Depends(oauth2_scheme)) -> dict[str, str]:
    # Decode to obtain expiry for bookkeeping; if decode fails, still accept logout
    exp = datetime.now(timezone.utc)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if "exp" in payload:
            exp = datetime.fromtimestamp(payload["exp"], timezone.utc)  # type: ignore[arg-type]
    except JWTError:
        pass
    await TokenBlacklist.get_or_create(token=token, defaults={"expired_at": exp})
    return {"message": "Logged out"}


@app.get("/api/users/me", response_model=UserResponse)
async def me(user: User = Depends(get_current_user)) -> UserResponse:
    return UserResponse(
        id=user.id, email=user.email, nickname=user.nickname, created_at=user.created_at
    )


# Note: Non-auth feature endpoints (diaries, quotes/bookmarks, questions)
# will be implemented by teammates. Only auth is included here.
