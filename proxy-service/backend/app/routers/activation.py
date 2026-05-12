from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import auth, crud, schemas
from app.database import get_db
from app.config import settings
from app.websocket_manager import status_manager

router = APIRouter()


@router.post("/activate-key", response_model=schemas.DesktopSessionResponse)
async def activate_key(
    request: schemas.ActivateKeyRequest,
    db: Session = Depends(get_db),
):
    user = crud.get_user_by_activation_key(db, request.key)
    if user is None:
        raise HTTPException(status_code=400, detail="Invalid activation key")

    if user.activation_key_expires and user.activation_key_expires < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Activation key expired")

    assigned_vm = crud.get_assigned_vm_for_user(db, user.id)
    if assigned_vm is not None:
        crud.consume_activation_key(db, user)
        desktop_token = auth.create_access_token(
            {"sub": str(user.id)},
            expires_minutes=settings.DESKTOP_TOKEN_EXPIRE_MINUTES,
            token_type="desktop",
        )
        await status_manager.broadcast_status(
            user.id,
            "connected",
            f"Reconnected to {assigned_vm.name}",
            assigned_vm,
        )
        ws_url = f"{settings.PUBLIC_WS_BASE_URL}/ws/status?token={desktop_token}"
        return schemas.DesktopSessionResponse(
            user_id=user.id,
            host=assigned_vm.host,
            port=assigned_vm.port,
            protocol=assigned_vm.protocol,
            token_type="bearer",
            access_token=desktop_token,
            ws_url=ws_url,
            status="connected",
            message=f"Reconnected to {assigned_vm.name}",
        )

    free_vm = crud.allocate_vm_to_user(db, user)
    if free_vm is None:
        await status_manager.broadcast_status(
            user.id,
            "no_free_vms",
            "All proxy servers are busy right now",
        )
        raise HTTPException(status_code=503, detail="All proxy servers are busy")

    desktop_token = auth.create_access_token(
        {"sub": str(user.id)},
        expires_minutes=settings.DESKTOP_TOKEN_EXPIRE_MINUTES,
        token_type="desktop",
    )
    await status_manager.broadcast_status(
        user.id,
        "connected",
        f"Connected to {free_vm.name}",
        free_vm,
    )
    ws_url = f"{settings.PUBLIC_WS_BASE_URL}/ws/status?token={desktop_token}"

    return schemas.DesktopSessionResponse(
        user_id=user.id,
        host=free_vm.host,
        port=free_vm.port,
        protocol=free_vm.protocol,
        token_type="bearer",
        access_token=desktop_token,
        ws_url=ws_url,
        status="connected",
        message=f"Connected to {free_vm.name}",
    )


@router.post("/disconnect", response_model=schemas.MessageResponse)
async def disconnect_proxy(
    current_user=Depends(auth.get_current_desktop_user),
    db: Session = Depends(get_db),
):
    released_vm = crud.release_vm_for_user(db, current_user.id)
    if released_vm is None:
        await status_manager.broadcast_status(
            current_user.id,
            "disconnected",
            "No active proxy connection",
        )
        return schemas.MessageResponse(
            message="No active proxy connection",
            status="disconnected",
        )

    await status_manager.broadcast_status(
        current_user.id,
        "disconnected",
        f"Disconnected from {released_vm.name}",
    )
    return schemas.MessageResponse(
        message=f"Disconnected from {released_vm.name}",
        status="disconnected",
    )
