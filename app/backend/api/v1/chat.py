from fastapi import APIRouter
from schemas.chat import PromptRequest, PromptResponse
from services.ollama import ask_ollama

router = APIRouter()

@router.post("/chat", response_model=PromptResponse)
async def chat(req: PromptRequest):
    result = await ask_ollama(req.prompt)
    return PromptResponse(response=result)