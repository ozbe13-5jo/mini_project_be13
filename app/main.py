from fastapi import FastAPI
from app.core.config import settings
app = FastAPI(title=settings.APP_NAME, version="0.1.0")
@app.get("/")
def read_root():
    return {"message": f"Hello from {settings.APP_NAME} ({settings.ENV})"}
