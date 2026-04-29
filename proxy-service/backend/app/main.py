from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, profile, activation
from app.database import engine
from app import models

# заменить на Alembic для миграций
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Proxy Service API", docs_url="/docs")

# CORS для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:80"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(profile.router, prefix="/api", tags=["profile"])
app.include_router(activation.router, prefix="/api", tags=["activation"])

@app.get("/health")
async def health():
    return {"status": "ok"}