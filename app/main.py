from fastapi import FastAPI
from app.core.config import settings
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
# from models import User
# from schemas import UserCreate, UserRead



app = FastAPI(title=settings.APP_NAME, version="0.1.0")
@app.get("/")
def read_root():
    return {"message": f"Hello from {settings.APP_NAME} ({settings.ENV})"}
