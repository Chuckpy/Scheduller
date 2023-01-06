from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Header, Path
from sqlalchemy.orm import Session
from database.db import get_session

from core.apps.auth.services.user_services import UserController
from .services.connection_manager import ConnectionManager


user_controller = UserController()
manager = ConnectionManager()


router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.on_event("startup")
async def startup():
    # Prime the push notification generator
    await manager.generator.asend(None)


@router.websocket("/")
async def websocket_endpoint(
    # room_id: Path(),
    websocket: WebSocket,
    session: Session = Depends(get_session),
    authorization: str
    | None = Header(
        default="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXJuYW1lIiwiZXhwIjoxNjcyOTQ4MTc4fQ.eTxyWKl7TsOvSH4fzrco__ZzB4ylUUx2bOfauTHSo88"
    ),
):

    user = user_controller._get_user(authorization, session)

    await manager.connect(websocket, user.id)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{user.first_name} diz: {data}")

    except WebSocketDisconnect:
        await manager.remove(websocket, user.id)
        await manager.broadcast(f"{user.first_name} left the chat")
