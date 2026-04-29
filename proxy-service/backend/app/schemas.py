from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    activation_key: Optional[str] = None
    is_active: bool
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class ActivateKeyRequest(BaseModel):
    key: str

class ProxyResponse(BaseModel):
    host: str
    port: int
    protocol: str

class ChangePassword(BaseModel):
    old_password: str
    new_password: str

class RefreshKeyResponse(BaseModel):
    message: str
    activation_key: str