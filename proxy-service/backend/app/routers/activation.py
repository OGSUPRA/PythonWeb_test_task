from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app import schemas, models, auth
from app.database import get_db

router = APIRouter()

@router.post("/activate-key", response_model=schemas.ProxyResponse)
def activate_key(
    request: schemas.ActivateKeyRequest,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    # Проверка ключа
    if current_user.activation_key != request.key:
        raise HTTPException(status_code=400, detail="Invalid activation key")
    
    if current_user.activation_key_expires < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Activation key expired")
    
    # Ищем свободную виртуалку
    free_vm = db.query(models.VirtualMachine).filter(
        models.VirtualMachine.current_user_id.is_(None),
        models.VirtualMachine.is_active == True
    ).first()
    
    if not free_vm:
        raise HTTPException(status_code=503, detail="No free proxy servers available")
    
    # Занимаем виртуалку
    free_vm.current_user_id = current_user.id
    free_vm.last_used_at = datetime.utcnow()
    db.commit()
    
    # Помечаем ключ как использованный
    current_user.activation_key = None
    current_user.activation_key_expires = None
    db.commit()
    
    return schemas.ProxyResponse(
        host=free_vm.host,
        port=free_vm.port,
        protocol=free_vm.protocol
    )