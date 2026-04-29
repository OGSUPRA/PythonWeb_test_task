from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    activation_key = Column(String, unique=True, index=True, nullable=True)
    activation_key_expires = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class VirtualMachine(Base):
    __tablename__ = "virtual_machines"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    host = Column(String, nullable=False)
    port = Column(Integer, nullable=False)
    protocol = Column(String, nullable=False)  # socks5, http, https
    is_active = Column(Boolean, default=True)
    current_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    last_used_at = Column(DateTime, nullable=True)