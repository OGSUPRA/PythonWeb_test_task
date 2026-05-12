from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")
security = HTTPBearer()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    if len(password.encode("utf-8")) > 72:
        raise ValueError("Password is too long for bcrypt_sha256")
    return pwd_context.hash(password)


def create_access_token(
    data: dict,
    *,
    expires_minutes: Optional[int] = None,
    token_type: str = "access",
):
    to_encode = data.copy()
    expire_minutes = expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
    to_encode.update({"exp": expire, "token_type": token_type})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload


def get_user_from_token(
    token: str,
    db: Session,
    *,
    required_token_type: Optional[str] = None,
):
    payload = decode_token(token)
    token_type = payload.get("token_type", "access")
    if required_token_type and token_type != required_token_type:
        raise HTTPException(status_code=403, detail="Wrong token type")

    user_id = payload["sub"]
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User is inactive")
    return user


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    return get_user_from_token(
        credentials.credentials,
        db,
        required_token_type="access",
    )


def get_current_desktop_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    return get_user_from_token(
        credentials.credentials,
        db,
        required_token_type="desktop",
    )
