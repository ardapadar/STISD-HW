import time
import logging
from fastapi import FastAPI, Request, Security, HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader
from fastapi.staticfiles import StaticFiles
from app.api.endpoints import router as note_router
from app.db.database import engine, Base


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Special Topics in Software Development HW-Production")


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Special Topics in Software Development HW Notes Pro")


API_KEY = "secret_key_2024"
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

async def verify_api_key(header: str = Security(api_key_header)):
    if header != API_KEY:
        raise HTTPException(status_code=403, detail="Yetkisiz Erişim!")
    return header


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"Yol: {request.url.path} | Süre: {duration:.4f}s")
    return response


app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(note_router, prefix="/api/v1/notes", tags=["Notes"], dependencies=[Depends(verify_api_key)])

@app.get("/")
def home():
    return {"status": "Special Topics in Software Development AI API Online", "ui": "/static/index.html"}