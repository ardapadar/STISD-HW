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

logger = logging.getLogger("Notes-API")
router = APIRouter()
security = HTTPBearer()

NOTIFICATION_SERVICE_URL = "http://notification-service:8001/send-email"

def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Oturum açmanız gerekiyor"
        )
    return token.credentials



@router.get("/", response_model=List[schemas.NoteResponse])
def get_notes(db: Session = Depends(get_db), user_token: str = Depends(get_current_user)):
    return note_service.list_notes(db)

@router.post("/", response_model=schemas.NoteResponse)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db), user_token: str = Depends(get_current_user)):
    return note_service.create_new_note(db, note)

@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db), user_token: str = Depends(get_current_user)):
    if not note_service.delete_note(db, note_id):
        raise HTTPException(status_code=404, detail="Not bulunamadı")
    return {"status": "success"}



@router.post("/analyze-cognition", response_model=schemas.AnalysisResponse)
async def analyze_cognition(data: schemas.AnalysisRequest, user_token: str = Depends(get_current_user)):
    """Frontend'deki 5 soruluk testin sonuçlarını işleyen derin analiz motoru."""
    ans = data.answers

    scores = [70, 70, 70] 
    
   
    if ans.get("q1") == "often":
        scores[0] -= 30
    else:
        scores[0] += 20

    if ans.get("q2") == "short":
        scores[1] -= 25
        scores[2] += 20 
    else:
        scores[1] += 25

    
    if ans.get("q3") == "daily":
        scores[0] += 15
    else:
        scores[0] -= 10

   
    if ans.get("q4") == "messy":
        scores[1] -= 15
    
   
    logic_score = 0
    if ans.get("q5") == "logic":
        logic_score += 40
        brain_balance = "Left-Brained (Analytical)"
    else:
        logic_score -= 40
        brain_balance = "Right-Brained (Creative)"

    
    scores = [max(0, min(100, s)) for s in scores]

    
    recommendations = []
    if scores[0] < 50:
        recommendations.append("Hatırlama oranını artırmak için notlarına 'Önemli' bayrağı ekle.")
    if scores[1] < 50:
        recommendations.append("Detayları kaçırmamak için AI Özetleme özelliğini kullan.")
    if not recommendations:
        recommendations.append("Harika bir dengeye sahipsin. Bu şekilde devam et!")

    return {
        "brain_balance": brain_balance,
        "memory_score": scores,
        "recommendation": " ".join(recommendations),
        "insight_text": "Bilişsel Profiliniz Analiz Edildi."
    }



@router.get("/stats", response_model=schemas.NoteStatsResponse)
def get_note_stats(db: Session = Depends(get_db), user_token: str = Depends(get_current_user)):
    try:
        total = db.query(models.Note).count()
        if total == 0:
            return {
                "total_notes": 0, "important_count": 0, "category_distribution": [],
                "ai_insight": "Henüz notun yok, analiz için biraz yazmalısın!", "focus_alert": False
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
        ai_insight = f"Zihniniz şu an en çok **{top_cat}** kategorisiyle meşgul."

        return {
            "total_notes": total,
            "important_count": important_count,
            "category_distribution": category_list,
            "ai_insight": ai_insight,
            "focus_alert": (important_count > total / 2)
        }
    except Exception as e:
        logger.error(f"Stats Error: {e}")
        raise HTTPException(status_code=500, detail="İstatistik hatası")



@router.post("/{note_id}/share")
async def share_note(
    note_id: int, 
    share_req: schemas.NoteShareRequest, 
    db: Session = Depends(get_db), 
    user_token: str = Depends(get_current_user)
):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Not bulunamadı")
    
    async with httpx.AsyncClient() as client:
        try:
            payload = {"email": share_req.email, "title": note.title, "content": note.content}
            response = await client.post(NOTIFICATION_SERVICE_URL, json=payload, timeout=5.0)
            
            if response.status_code == 200:
                return {"status": "success", "message": "E-posta başarıyla gönderildi."}
            else:
                raise HTTPException(status_code=500, detail="Bildirim servisi hatası.")
        except Exception as e:
            logger.error(f"Comm Error: {e}")
            raise HTTPException(status_code=503, detail="E-posta servisi şu an kullanılamıyor.")