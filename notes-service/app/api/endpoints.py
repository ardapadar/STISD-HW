import requests
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import models
from app.api import note_schema
from app.core import note_service
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()


security = HTTPBearer()

def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)):
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Oturum açmanız gerekiyor"
        )
    return token.credentials



@router.get("/", response_model=list[note_schema.NoteResponse])
def get_notes(
    db: Session = Depends(get_db),
    user_token: str = Depends(get_current_user)
):
    return note_service.list_notes(db)

@router.post("/", response_model=note_schema.NoteResponse)
def create_note(
    note: note_schema.NoteCreate, 
    db: Session = Depends(get_db),
    user_token: str = Depends(get_current_user)
):
    return note_service.create_new_note(db, note)

@router.delete("/{note_id}")
def delete_note(
    note_id: int, 
    db: Session = Depends(get_db),
    user_token: str = Depends(get_current_user)
):
    if not note_service.delete_note(db, note_id):
        raise HTTPException(status_code=404, detail="Not bulunamadı")
    return {"status": "success"}



@router.post("/{note_id}/share")
async def share_note(
    note_id: int, 
    email_request: dict, 
    db: Session = Depends(get_db),
    user_token: str = Depends(get_current_user)
):
   
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Not bulunamadı")
    
    target_email = email_request.get("email")
    if not target_email:
        raise HTTPException(status_code=400, detail="Mail adresi gerekli")

    
    try:
        notification_payload = {
            "email": target_email,
            "title": note.title,
            "content": note.content
        }
        
        
        response = requests.post(
            "http://notification-service:8001/send-email", 
            json=notification_payload, 
            timeout=3
        )
        
        if response.status_code == 200:
            return {"status": "success", "message": f"Not {target_email} adresine iletildi."}
        else:
            raise HTTPException(status_code=500, detail="Haberci servisi hata verdi.")

    except Exception as e:
        
        raise HTTPException(status_code=500, detail=f"Servisler arası iletişim hatası: {str(e)}")