from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from services.fix_message import FixMessageService
from services.response import ResponseMessageService

router = APIRouter()

@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            if data['action'] == 'fix':
                response_fix = await FixMessageService(data['message']).fix_message()
                await websocket.send_json(response_fix)
            elif data['action'] == 'response':
                response_response = await ResponseMessageService(data['message']).respond()
                await websocket.send_json(response_response)
    except WebSocketDisconnect:
        print("Cliente desconectado")
    except Exception as e:
        print(f"Error en el WebSocket: {str(e)}")