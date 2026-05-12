from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app import crud, models
from app.config import settings
from app.database import SessionLocal, engine
from app.routers import activation, auth, profile, websocket

# TODO: replace with Alembic migrations in a production-grade version.
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Proxy Service API", docs_url="/docs")

# CORS for the browser frontend and Electron desktop client.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:80",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "null",
        "file://",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(profile.router, prefix="/api", tags=["profile"])
app.include_router(activation.router, prefix="/api", tags=["activation"])
app.include_router(websocket.router, tags=["websocket"])


@app.on_event("startup")
def seed_virtual_machine_pool():
    if not settings.AUTO_SEED_VMS:
        return

    db: Session = SessionLocal()
    try:
        crud.seed_virtual_machines(db)
    finally:
        db.close()


@app.get("/health")
async def health():
    return {"status": "ok"}
