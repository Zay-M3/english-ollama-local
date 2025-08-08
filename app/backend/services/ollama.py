import httpx
from config import OLLAMA_API_URL
import asyncio

ollama_semaphore = asyncio.Semaphore(1)  # Limit concurrent requests to 1

async def ask_ollama(prompt:str) -> str:
    async with ollama_semaphore:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(OLLAMA_API_URL, 
                json={
                    'model': "mistral",
                    "prompt": prompt,
                    'stream': False
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
    prompt = f'Friendly English teacher: Spot grammar or word mistakes in "{message}", explain simply, and show the fun corrected version. If perfect, say "Looks great!". Max 15 words.'
    max_attempts = 3
    for attempt in range(max_attempts):
        async with ollama_semaphore:
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.post(OLLAMA_API_URL, 
                    json={
                        'model': "mistral",
                        "prompt": prompt,
                        'stream': False,
                        'options': {
                            'temperature': 0.3,
                            'top_p': 0.9,
                            'max_tokens': 60,
                        }
                        },
                        timeout = 8 + (attempt * 3)
                    )
                    response.raise_for_status()
                    data = response.json()
                    return data.get('response', 'no response')
                
                except httpx.TimeoutException:
                    if attempt < max_attempts - 1:
                        await asyncio.sleep(1.5 ** attempt)  
                        continue
                    else:
                        return "Response timeout - please try again"

                except httpx.RequestError as e:
                    return f"Request error: {str(e)}"
                except Exception as e:
                    return f"An unexpected error occurred: {str(e)}"
    


# ask_llama_response para responder al mensaje enviado 
async def ask_llama_response(message: str) -> str:
    prompt = f'Reply to "{message}" with a fun, creative answer (max 15 words). Ask a playful question or invite the user to keep chatting.'
    max_attempts = 3
    for attempt in range(max_attempts):
        async with ollama_semaphore:
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.post(OLLAMA_API_URL, 
                    json={
                        'model': "mistral",
                        "prompt": prompt,
                        'stream': False,
                        
                        'options': {
                            'temperature': 0.3,
                            'top_p': 0.9,
                            'max_tokens': 60,
                        }
                        },
                        timeout = 8 + (attempt * 3) 
                    )
                    response.raise_for_status()
                    data = response.json()
                    return data.get('response', 'no response')
                
                except httpx.TimeoutException:
                    if attempt < max_attempts - 1:
                        await asyncio.sleep(1.5 ** attempt)  
                        continue
                    else:
                        return "Response timeout - please try again"
                
                except httpx.RequestError as e:
                    return f"Request error: {str(e)}"
                except Exception as e:
                    return f"An unexpected error occurred: {str(e)}"
