from fastapi import APIRouter, WebSocket, WebSocketDisconnect


router = APIRouter()

@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Mensaje recibido: {data}")
            await websocket.send_text(f"Mensaje recibido: {data}")
    except WebSocketDisconnect:
        print("Cliente desconectado")
    except Exception as e:
        print(f"Error en el WebSocket: {str(e)}")