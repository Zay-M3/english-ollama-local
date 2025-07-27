from fastapi import FastAPI
from pydantic import BaseModel
import httpx

app = FastAPI(
    title='backend',
    description='backend to websocket',
    version='1.0.0',
)

class Promt(BaseModel):
    prompt : str


@app.post("/chat")
async def Chat(req: Promt):
    async with httpx.AsyncClient(timeout=300) as client:
        try:
            response = await client.post(
                "http://localhost:11434/api/generate",
                json={
                    'model':"llama3",
                    'prompt':req.prompt,
                    'stream':False
                }
            )
            data = response.json()
            return {'response':data.get('response', 'no response')}
        except Exception as e:
            return {'error': 'An unexpected error occurred', 'details': str(e)}
