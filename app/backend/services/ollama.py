import httpx
from config import OLLAMA_API_URL

async def ask_ollama(prompt:str) -> str:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(OLLAMA_API_URL, 
            json={
                'model': "llama3",
                "prompt": prompt,
                'stream': False
                }
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
    prompt = f"Correct the following English message. Return only the corrected version:\n\n{message}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(OLLAMA_API_URL, 
            json={
                'model': "llama3",
                "prompt": prompt,
                'stream': False
                }
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
    prompt = f"Respond to the following English message:\n\n{message}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(OLLAMA_API_URL, 
            json={
                'model': "llama3",
                "prompt": prompt,
                'stream': False
                }
            )
            response.raise_for_status()
            data = response.json()
            return data.get('response', 'no response')
        
        except httpx.RequestError as e:
            return f"Request error: {str(e)}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"


