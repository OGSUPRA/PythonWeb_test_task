from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models, auth
from app.database import get_db
from app.tasks import send_activation_email_task
import secrets
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/profile", response_model=schemas.UserResponse)
def get_profile(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

@router.post("/refresh-key", response_model=schemas.RefreshKeyResponse)
def refresh_key(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    # Генерация нового ключа
    new_key = secrets.token_urlsafe(32)
    current_user.activation_key = new_key
    current_user.activation_key_expires = datetime.utcnow() + timedelta(days=7)
    db.commit()
    
    # Отправка на почту
    send_activation_email_task.delay(current_user.email, new_key)
    
    return {"message": "New key sent to email", "activation_key": new_key}

@router.post("/change-password")
def change_password(
    data: schemas.ChangePassword,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    if not auth.verify_password(data.old_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Wrong password")
    
    current_user.password_hash = auth.get_password_hash(data.new_password)
    db.commit()
    
    return {"message": "Password changed successfully"}