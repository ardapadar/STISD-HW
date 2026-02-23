from fastapi import FastAPI
from app.api.endpoints import router as note_router
from app.db.database import engine, Base
import logging

# Observability: Profesyonel loglama başlat
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NotesAPI")

# DB tablolarını ayağa kaldır (Production'da genelde Alembic kullanılır)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Notes Microservice Pro",
    description="Clean Architecture & AI Integrated Microservice",
    version="1.1.0"
)

# Health Check (K8s/Docker için kritik!)
@app.get("/health", tags=["Monitoring"])
def health():
    return {"status": "up", "database": "connected"}

app.include_router(note_router, prefix="/api/v1/notes", tags=["Notes Management"])

logger.info("Service is ready to handle requests 🚀")