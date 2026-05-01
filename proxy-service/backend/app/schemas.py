from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime

PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 72

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str

    @field_validator('password', 'confirm_password')
    def validate_password_length(cls, v):
        byte_length = len(v.encode('utf-8'))
        if byte_length > PASSWORD_MAX_LENGTH:
            raise ValueError(
                f'Password too long: {byte_length} bytes (max {PASSWORD_MAX_LENGTH})'
            )
        if byte_length < PASSWORD_MIN_LENGTH:
            raise ValueError(
                f'Password too short: {byte_length} bytes (min {PASSWORD_MIN_LENGTH})'
            )
        return v

    @field_validator('confirm_password')
    def validate_passwords_match(cls, v, info):
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('Passwords do not match')
        return v

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

    @field_validator('old_password', 'new_password')
    def validate_password_length(cls, v):
        byte_length = len(v.encode('utf-8'))
        if byte_length > PASSWORD_MAX_LENGTH:
            raise ValueError(
                f'Password too long: {byte_length} bytes (max {PASSWORD_MAX_LENGTH})'
            )
        if byte_length < PASSWORD_MIN_LENGTH:
            raise ValueError(
                f'Password too short: {byte_length} bytes (min {PASSWORD_MIN_LENGTH})'
            )
        return v

class RefreshKeyResponse(BaseModel):
    message: str
    activation_key: str