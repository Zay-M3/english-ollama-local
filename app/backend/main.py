from fastapi import FastAPI
from api.v1 import chat, websocker

app = FastAPI()

app.include_router(chat.router, prefix="/api/v1")
app.include_router(websocker.router)

