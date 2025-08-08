import pytest
from unittest.mock import patch, MagicMock
from services.fix_message import FixMessageService
from services.response import ResponseMessageService


class TestFixMessageService:
    """Tests para el servicio de corrección de mensajes"""

    @pytest.mark.asyncio
    async def test_fix_message_success(self):
        """Test exitoso de corrección"""
        service = FixMessageService("I are good")
        
        # Mock de ask_llama_fix
        with patch('services.fix_message.ask_llama_fix') as mock_fix:
            mock_fix.return_value = "I am good"
            
            result = await service.fix_message()
            
            assert result["type"] == "fix"
            assert result["original"] == "I are good"
            assert result["content"] == "I am good"
            assert result["fixmessage"] is True

    @pytest.mark.asyncio
    async def test_fix_message_empty_input(self):
        """Test con mensaje vacío"""
        service = FixMessageService("")
        
        result = await service.fix_message()
        
        assert "error" in result
        assert result["error"] == "Empty message"

    @pytest.mark.asyncio
    async def test_fix_message_too_long(self):
        """Test con mensaje demasiado largo"""
        long_message = "a" * 1001
        service = FixMessageService(long_message)
        
        result = await service.fix_message()
        
        assert "error" in result
        assert "too long" in result["error"].lower()

    @pytest.mark.asyncio
    async def test_fix_message_exception(self):
        """Test cuando ocurre una excepción"""
        service = FixMessageService("test message")
        
        with patch('services.fix_message.ask_llama_fix') as mock_fix:
            mock_fix.side_effect = Exception("Connection error")
            
            result = await service.fix_message()
            
            assert "error" in result
            assert "Connection error" in result["error"]


class TestResponseMessageService:
    """Tests para el servicio de respuesta de mensajes"""

    @pytest.mark.asyncio
    async def test_respond_success(self):
        """Test exitoso de respuesta"""
        service = ResponseMessageService("Hello")
        
        with patch('services.response.ask_llama_response') as mock_response:
            mock_response.return_value = "Hi there! How can I help you?"
            
            result = await service.respond()
            
            assert result["type"] == "response"
            assert result["original"] == "Hello"
            assert result["content"] == "Hi there! How can I help you?"
            assert result["fixmessage"] is False

    @pytest.mark.asyncio
    async def test_respond_empty_input(self):
        """Test con mensaje vacío"""
        service = ResponseMessageService("   ")  # Solo espacios
        
        result = await service.respond()
        
        assert "error" in result
        assert result["error"] == "Empty message"

    @pytest.mark.asyncio
    async def test_respond_too_long(self):
        """Test con mensaje demasiado largo"""
        long_message = "hello " * 200  # Más de 1000 caracteres
        service = ResponseMessageService(long_message)
        
        result = await service.respond()
        
        assert "error" in result
        assert "too long" in result["error"].lower()

    @pytest.mark.asyncio
    async def test_respond_exception(self):
        """Test cuando ocurre una excepción"""
        service = ResponseMessageService("test")
        
        with patch('services.response.ask_llama_response') as mock_response:
            mock_response.side_effect = Exception("Model unavailable")
            
            result = await service.respond()
            
            assert "error" in result
            assert "Model unavailable" in result["error"]
