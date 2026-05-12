import asyncio
from typing import Optional

from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app import auth
from app.database import get_db
from app.websocket_manager import status_manager

router = APIRouter()


async def _serve_status_socket(
    websocket: WebSocket,
    token: str,
    db: Session,
    user_id: Optional[int] = None,
):
    user = auth.get_user_from_token(token, db, required_token_type="desktop")
    if user_id is not None and user.id != user_id:
        await websocket.close(code=1008, reason="Token does not match requested user")
        return

    await status_manager.connect(user.id, websocket)
    await status_manager.send_current_status(user.id, websocket)

    try:
        while True:
            try:
                await asyncio.wait_for(websocket.receive_text(), timeout=15)
            except asyncio.TimeoutError:
                await status_manager.send_current_status(user.id, websocket)
    except WebSocketDisconnect:
        status_manager.disconnect(user.id, websocket)


@router.websocket("/ws/status")
async def websocket_status(
    websocket: WebSocket,
    token: str = Query(...),
    db: Session = Depends(get_db),
):
    await _serve_status_socket(websocket, token, db)


@router.websocket("/ws/connection-status/{user_id}")
async def websocket_connection_status(
    websocket: WebSocket,
    user_id: int,
    token: str = Query(...),
    db: Session = Depends(get_db),
):
    await _serve_status_socket(websocket, token, db, user_id=user_id)
