from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from .services.connection_manager import ConnectionManager


router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


manager = ConnectionManager()


@router.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client says: {data}")

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client left the chat")
