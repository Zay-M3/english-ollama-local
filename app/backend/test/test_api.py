import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient
from fastapi import WebSocket
from main import app


class TestWebSocketEndpoint:
    """Tests para el endpoint de WebSocket"""

    def test_websocket_fix_action(self):
        """Test de acción 'fix' via WebSocket"""
        with TestClient(app) as client:
            with client.websocket_connect("/ws/chat") as websocket:
                # Enviar mensaje de corrección
                test_data = {
                    "action": "fix",
                    "message": "I are good"
                }
                
                with patch('api.v1.websocker.FixMessageService') as mock_service:
                    mock_instance = AsyncMock()
                    mock_instance.fix_message.return_value = {
                        "type": "fix",
                        "content": "I am good",
                        "fixmessage": True
                    }
                    mock_service.return_value = mock_instance
                    
                    websocket.send_json(test_data)
                    response = websocket.receive_json()
                    
                    assert response["type"] == "fix"
                    assert response["content"] == "I am good"
                    assert response["fixmessage"] is True

    def test_websocket_response_action(self):
        """Test de acción 'response' via WebSocket"""
        with TestClient(app) as client:
            with client.websocket_connect("/ws/chat") as websocket:
                test_data = {
                    "action": "response",
                    "message": "Hello"
                }
                
                with patch('api.v1.websocker.ResponseMessageService') as mock_service:
                    mock_instance = AsyncMock()
                    mock_instance.respond.return_value = {
                        "type": "response",
                        "content": "Hi there!",
                        "fixmessage": False
                    }
                    mock_service.return_value = mock_instance
                    
                    websocket.send_json(test_data)
                    response = websocket.receive_json()
                    
                    assert response["type"] == "response"
                    assert response["content"] == "Hi there!"
                    assert response["fixmessage"] is False

    def test_websocket_invalid_action(self):
        """Test con acción inválida"""
        with TestClient(app) as client:
            with client.websocket_connect("/ws/chat") as websocket:
                # Enviar acción no válida
                test_data = {
                    "action": "invalid",
                    "message": "test"
                }
                
                websocket.send_json(test_data)
                # WebSocket debería mantenerse conectado pero no enviar respuesta
                # para acciones no reconocidas


class TestChatAPI:
    """Tests para el API REST de chat"""

    def test_chat_endpoint_success(self):
        """Test exitoso del endpoint de chat"""
        with TestClient(app) as client:
            with patch('api.v1.chat.ask_ollama') as mock_ollama:
                mock_ollama.return_value = "Hello! How can I help you?"
                
                response = client.post(
                    "/api/v1/chat",
                    json={"prompt": "Hello"}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert data["response"] == "Hello! How can I help you?"

    def test_chat_endpoint_validation_error(self):
        """Test con datos inválidos"""
        with TestClient(app) as client:
            # Enviar sin prompt
            response = client.post("/api/v1/chat", json={})
            
            assert response.status_code == 422  

    def test_chat_endpoint_ollama_error(self):
        """Test cuando Ollama falla"""
        with TestClient(app) as client:
            with patch('api.v1.chat.ask_ollama') as mock_ollama:
                mock_ollama.return_value = "Request error: Connection failed"
                
                response = client.post(
                    "/api/v1/chat",
                    json={"prompt": "Hello"}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert "error" in data["response"].lower()
