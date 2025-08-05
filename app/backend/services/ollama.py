import httpx
from config import OLLAMA_API_URL

async def ask_ollama(prompt:str) -> str:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(OLLAMA_API_URL, 
            json={
                'model': "llama3",
                "prompt": prompt,
                'stream': True
                },
                timeout = 30
            )
            response.raise_for_status()
            data = response.json()
            return data.get('response', 'no response')
        
        except httpx.RequestError as e:
            return f"Request error: {str(e)}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"


# ask_llama para corregir mensajes
async def ask_llama_fix(message: str) -> str:
    prompt = f"""Correct the student's English message below. If it's already correct, reply: "The message is correct."
    Message: "{message}"

    Respond in this format:
    Corrected: [corrected text]
    Notes: [2-3 main grammar or spelling points, brief]"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(OLLAMA_API_URL, 
            json={
                'model': "llama3",
                "prompt": prompt,
                'stream': False
                },
                timeout = 20
            )
            response.raise_for_status()
            data = response.json()
            return data.get('response', 'no response')
        
        except httpx.RequestError as e:
            return f"Request error: {str(e)}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"


# ask_llama_response para responder al mensaje enviado 
async def ask_llama_response(message: str) -> str:
    prompt = f"""Reply as a friendly English partner to help practice. Be supportive, ask a follow-up, and use clear English. If there's a mistake, model the correct form in your reply. Max 2-3 sentences.

    Student: "{message}"
    Your reply:
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(OLLAMA_API_URL, 
            json={
                'model': "llama3",
                "prompt": prompt,
                'stream': False
                },
                timeout = 15
            )
            response.raise_for_status()
            data = response.json()
            return data.get('response', 'no response')
        
        except httpx.RequestError as e:
            return f"Request error: {str(e)}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"


