from fastapi import FastAPI
from api.v1.chat import router as chat_router

app = FastAPI()

app.include_router(chat_router, prefix="/api/v1")
