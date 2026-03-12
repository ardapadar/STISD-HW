import time
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware 
from fastapi.staticfiles import StaticFiles
from app.api.endpoints import router as note_router
from app.db.database import engine, Base


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Notes-Service")


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Notes Service - Microservice Edition")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"Yol: {request.url.path} | Süre: {duration:.4f}s")
    return response


app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(note_router) 

@app.get("/")
def home():
    return {"status": "Notes Service Online", "ui": "/static/index.html"}