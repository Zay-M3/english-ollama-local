import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from services.ollama import ask_llama_fix, ask_llama_response
import httpx


class TestOllamaServices:
    """Tests para los servicios de Ollama"""

    @pytest.mark.asyncio
    async def test_ask_llama_fix_success(self):
        """Test exitoso de corrección de mensaje"""
        # Mock de la respuesta HTTP
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"response": "Corrected: I am good"}
        
        # Mock del cliente HTTP
        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        
        with patch('httpx.AsyncClient') as mock_async_client:
            # Configurar el context manager
            mock_async_client.return_value.__aenter__.return_value = mock_client
            mock_async_client.return_value.__aexit__.return_value = None
            
            result = await ask_llama_fix("I are good")
            
            # Verificaciones
            assert result == "Corrected: I am good"
            mock_client.post.assert_called_once()

    @pytest.mark.asyncio
    async def test_ask_llama_fix_timeout(self):
        """Test de timeout en corrección de mensaje"""
        mock_client = AsyncMock()
        mock_client.post.side_effect = httpx.TimeoutException("Timeout")
        
        with patch('httpx.AsyncClient') as mock_async_client:
            mock_async_client.return_value.__aenter__.return_value = mock_client
            mock_async_client.return_value.__aexit__.return_value = None
            
            # Mock del sleep para acelerar el test
            with patch('asyncio.sleep'):
                result = await ask_llama_fix("test message")
                
                # Debe retornar mensaje de timeout después de 3 intentos
                assert result == "Response timeout - please try again"
                assert mock_client.post.call_count == 3

    @pytest.mark.asyncio
    async def test_ask_llama_fix_request_error(self):
        """Test de error de request en corrección"""
        mock_client = AsyncMock()
        mock_client.post.side_effect = httpx.RequestError("Connection failed")
        
        with patch('httpx.AsyncClient') as mock_async_client:
            mock_async_client.return_value.__aenter__.return_value = mock_client
            mock_async_client.return_value.__aexit__.return_value = None
            
            result = await ask_llama_fix("test message")
            
            assert "Request error: Connection failed" in result

    @pytest.mark.asyncio
    async def test_ask_llama_response_success(self):
        """Test exitoso de respuesta de mensaje"""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"response": "Hello! How are you doing?"}
        
        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        
        with patch('httpx.AsyncClient') as mock_async_client:
            mock_async_client.return_value.__aenter__.return_value = mock_client
            mock_async_client.return_value.__aexit__.return_value = None
            
            result = await ask_llama_response("Hello")
            
            assert result == "Hello! How are you doing?"
            mock_client.post.assert_called_once()

    @pytest.mark.asyncio
    async def test_ask_llama_response_timeout_with_retries(self):
        """Test de timeout con reintentos en respuesta"""
        mock_client = AsyncMock()
        
        # Primer intento falla, segundo intento funciona
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"response": "Success after retry"}
        
        mock_client.post.side_effect = [
            httpx.TimeoutException("Timeout"),
            mock_response
        ]
        
        with patch('httpx.AsyncClient') as mock_async_client:
            mock_async_client.return_value.__aenter__.return_value = mock_client
            mock_async_client.return_value.__aexit__.return_value = None
            
            with patch('asyncio.sleep'):
                result = await ask_llama_response("test")
                
                assert result == "Success after retry"
                assert mock_client.post.call_count == 2

    @pytest.mark.asyncio
    async def test_semaphore_limits_concurrent_requests(self):
        """Test que el semáforo limita requests concurrentes"""
        from services.ollama import ollama_semaphore
        
        # Verificar que el semáforo tiene límite de 1
        assert ollama_semaphore._value == 1
        
        # Mock para simular request lento
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"response": "test response"}
        
        async def slow_post(*args, **kwargs):
            await asyncio.sleep(0.1) 
            return mock_response
        
        mock_client = AsyncMock()
        mock_client.post = slow_post
        
        with patch('httpx.AsyncClient') as mock_async_client:
            mock_async_client.return_value.__aenter__.return_value = mock_client
            mock_async_client.return_value.__aexit__.return_value = None
            
            # Ejecutar dos requests concurrentes
            task1 = asyncio.create_task(ask_llama_fix("test1"))
            task2 = asyncio.create_task(ask_llama_fix("test2"))
            
            results = await asyncio.gather(task1, task2)
            
            # Ambos deben completarse exitosamente
            assert all("test response" in result for result in results)
