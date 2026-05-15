import httpx
import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.database import get_db
from app.db import models
from app.api import note_schema as schemas 
from app.core import note_service
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

logger = logging.getLogger("Kawien-API")
router = APIRouter()
security = HTTPBearer()

# Microservice URL for the notification engine
NOTIFICATION_SERVICE_URL = "http://notification-service:8001/send-email"

def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired. Please re-authenticate."
        )
    return token.credentials

@router.get("/", response_model=List[schemas.NoteResponse])
def get_notes(db: Session = Depends(get_db), user_token: str = Depends(get_current_user)):
    return note_service.list_notes(db)

@router.post("/", response_model=schemas.NoteResponse)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db), user_token: str = Depends(get_current_user)):
    try:
        return note_service.create_new_note(db, note)
    except Exception as e:
        logger.error(f"Sync Error: {e}")
        raise HTTPException(status_code=500, detail="Neural Link Error: Could not save thought.")

@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db), user_token: str = Depends(get_current_user)):
    if not note_service.delete_note(db, note_id):
        raise HTTPException(status_code=404, detail="Thought node not found.")
    return {"status": "success", "message": "Node terminated."}

@router.post("/analyze-cognition", response_model=schemas.AnalysisResponse)
async def analyze_cognition(data: schemas.AnalysisRequest, user_token: str = Depends(get_current_user)):
    """
    Processes behavioral profiling data and returns English recommendations.
    Matches the Luxury Dashboard visualization.
    """
    try:
        analysis = note_service.analyze_cognitive_activity(data.answers)
        
        # Mapping scores to [Retention, Detail, Speed] for Chart.js
        scores = [
            analysis["scores"]["left"] * 15,
            analysis["scores"]["right"] * 12,
            (analysis["scores"]["left"] + analysis["scores"]["right"]) * 7
        ]
        scores = [max(0, min(100, s)) for s in scores]

        return {
            "brain_balance": analysis["target_region"],
            "memory_score": scores,
            "recommendation": f"Exercise: {analysis['recommended_exercise']} | Supplement: {analysis['supplement']}",
            "insight_text": analysis["scientific_rationale"]
        }
    except Exception as e:
        logger.error(f"Neural Analysis Error: {e}")
        raise HTTPException(status_code=500, detail="Cognitive Engine Timeout.")

@router.get("/stats", response_model=schemas.NoteStatsResponse)
def get_note_stats(db: Session = Depends(get_db), user_token: str = Depends(get_current_user)):
    try:
        total = db.query(models.Note).count()
        if total == 0:
            return {
                "total_notes": 0, "important_count": 0, "category_distribution": [],
                "ai_insight": "Ecosystem is empty. Start capturing thoughts.", "focus_alert": False
            }

        stats = db.query(models.Note.category, func.count(models.Note.id)).group_by(models.Note.category).all()
        
        category_list = []
        for cat, count in stats:
            category_list.append({
                "category": cat or "General",
                "count": count,
                "percentage": round((count / total) * 100, 2)
            })

        important_count = db.query(models.Note).filter(models.Note.is_important == True).count()
        top_cat = max(category_list, key=lambda x: x['count'])['category']
        
        return {
            "total_notes": total,
            "important_count": important_count,
            "category_distribution": category_list,
            "ai_insight": f"Your neural focus is currently on **{top_cat}**.",
            "focus_alert": (important_count > total / 2)
        }
    except Exception as e:
        logger.error(f"Stats Processing Error: {e}")
        raise HTTPException(status_code=500, detail="Data visualization failed.")

@router.post("/{note_id}/share")
async def share_note(
    note_id: int, 
    share_req: schemas.NoteShareRequest, 
    db: Session = Depends(get_db), 
    user_token: str = Depends(get_current_user)
):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Thought not found.")
    
    async with httpx.AsyncClient() as client:
        try:
            payload = {"email": share_req.email, "title": note.title, "content": note.content}
            response = await client.post(NOTIFICATION_SERVICE_URL, json=payload, timeout=5.0)
            
            if response.status_code == 200:
                return {"status": "success", "message": "Neural data transmitted via email."}
            else:
                raise HTTPException(status_code=500, detail="Notification Microservice unreachable.")
        except Exception as e:
            logger.error(f"Transmission Error: {e}")
            raise HTTPException(status_code=503, detail="Email Gateway Offline.")