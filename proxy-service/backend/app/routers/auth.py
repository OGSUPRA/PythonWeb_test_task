from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, models, auth
from app.database import get_db
from app.tasks import send_activation_email_task
import secrets
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserRegister, db: Session = Depends(get_db)):
    # Проверка пароля
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords don't match")
    
    # Проверка email
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Создание пользователя
    activation_key = secrets.token_urlsafe(32)
    db_user = models.User(
        email=user.email,
        password_hash=auth.get_password_hash(user.password),
        activation_key=activation_key,
        activation_key_expires=datetime.utcnow() + timedelta(days=7)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Отправка письма (асинхронно через Celery)
    send_activation_email_task.delay(user.email, activation_key)
    
    return db_user

@router.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not auth.verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = auth.create_access_token(data={"sub": str(db_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}