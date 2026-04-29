#Для локальной разработки и тестирования
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://admin:admin@postgres:5432/proxy_db"
    REDIS_URL: str = "redis://redis:6379/0"
    SECRET_KEY: str = "super-secret-key" #Заменить на более сложный ключ в продакшене
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60*24*7  # 7 дней
    
    SMTP_HOST: str = "smtp.mailtrap.io"
    SMTP_PORT: int = 2525
    SMTP_USER: str = "mailtrap_username" #Заменить на реальные данные от Mailtrap
    SMTP_PASSWORD: str = "mailtrap_password" #Заменить на реальные данные от Mailtrap
    
    class Config:
        env_file = ".env"

settings = Settings()