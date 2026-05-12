# Для локальной разработки и тестирования
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://admin:admin@postgres:5432/proxy_db"
    REDIS_URL: str = "redis://redis:6379/0"

    SECRET_KEY: str = "super-secret-key"  # Заменить на более сложный ключ в продакшене
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    DESKTOP_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    EMAIL_BACKEND: str = "console"
    SMTP_HOST: str = "smtp.mailtrap.io"
    SMTP_PORT: int = 2525
    SMTP_USER: str = "mailtrap_username"
    SMTP_PASSWORD: str = "mailtrap_password"
    SMTP_FROM_EMAIL: str = "no-reply@proxy-service.local"
    SMTP_USE_TLS: bool = True

    PUBLIC_WS_BASE_URL: str = "ws://localhost:8000"
    AUTO_SEED_VMS: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
