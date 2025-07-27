from fastapi import APIRouter
from schemas.chat import promtRequest, promtResponse
from services.ollama import ask_ollama

router = APIRouter()

@router.post("/chat", response_model=promtResponse)
async def chat(req: promtRequest):
    result = await ask_ollama(req.prompt)
    return promtResponse(response=result)