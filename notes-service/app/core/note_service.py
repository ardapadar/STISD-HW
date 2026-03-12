import requests 
import logging
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db import models
from app.api import note_schema


logger = logging.getLogger("UYG414-Core")

def analyze_note_with_ai(content: str):
    
    text = content.lower()
    
  
    categories = {
        "Eğitim/Akademik": ["sınav", "ödev", "vize", "final", "ders", "okul", "proje"],
        "İş ve Kariyer": ["toplantı", "mail", "sunum", "ofis", "müşteri", "rapor"],
        "Kişisel Acil": ["acil", "hemen", "dikkat", "doktor", "randevu", "deadline"],
        "Günlük/Genel": ["market", "belki", "alışveriş", "yemek", "kitap"]
    }
    
    found_category = "Genel Not"
    score = 0
    
    for cat, words in categories.items():
        if any(word in text for word in words):
            found_category = cat
            if cat == "Kişisel Acil": score = 95
            elif cat == "Eğitim/Akademik": score = 85
            elif cat == "İş ve Kariyer": score = 75
            else: score = 40
            break

    ai_report = f"[{found_category}] Odaklı: {content[:30]}..." if len(content) > 30 else f"{found_category}: {content}"
    is_imp_ai = score >= 75
    return is_imp_ai, score, ai_report

def create_new_note(db: Session, note: note_schema.NoteCreate):
   
    
    is_imp_ai, score, summary = analyze_note_with_ai(note.content)
    
  
    db_note = models.Note(
        title=note.title,
        content=note.content,
        category=note.category,
        bg_color=note.bg_color,
        is_important=note.is_important or is_imp_ai, 
        importance_score=score,
        ai_summary=summary
    )
    
    
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    
    logger.info(f"Yeni Not Oluşturuldu: {note.title} (Kategori: {note.category})")

  
    if db_note.is_important:
        try:
            notification_url = "http://notification-service:8001/notify"
            payload = {
                "title": db_note.title,
                "category": db_note.category
            }
          
            requests.post(notification_url, json=payload, timeout=2)
            logger.info("Notification Service başarıyla tetiklendi.")
        except Exception as e:
          
            logger.error(f"Notification Service'e ulaşılamadı: {e}")

    return db_note

def list_notes(db: Session):
   
    return db.query(models.Note).order_by(desc(models.Note.is_important), desc(models.Note.id)).all()

def delete_note(db: Session, note_id: int):
   
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if note:
        db.delete(note)
        db.commit()
        return True
    return False