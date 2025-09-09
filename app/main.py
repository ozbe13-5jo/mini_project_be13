from fastapi import FastAPI
from app.routers import diary, auth

app = FastAPI()

app.include_router(auth.router)
app.include_router(diary.router)

