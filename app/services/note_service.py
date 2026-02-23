from sqlalchemy.orm import Session
from app.models.note import Note
from app.schemas.note_schema import NoteCreate, NoteUpdate
from fastapi import HTTPException, status

class NoteService:
    @staticmethod
    def get_all(db: Session):
        return db.query(Note).all()

    @staticmethod
    def create(db: Session, note_in: NoteCreate):
        db_note = Note(**note_in.model_dump())
        db.add(db_note)
        db.commit()
        db.refresh(db_note)
        return db_note

    @staticmethod
    def update(db: Session, note_id: int, note_in: NoteUpdate):
        db_note = db.query(Note).filter(Note.id == note_id).first()
        if not db_note:
            raise HTTPException(status_code=404, detail="Not bulunamadı.")
        
        update_data = note_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_note, field, value)
        
        db.commit()
        db.refresh(db_note)
        return db_note

    @staticmethod
    def delete(db: Session, note_id: int):
        db_note = db.query(Note).filter(Note.id == note_id).first()
        if not db_note:
            raise HTTPException(status_code=404, detail="Böyle bir not yok.")
        db.delete(db_note)
        db.commit()
        return {"detail": "Başarıyla silindi"}

    @staticmethod
    def ai_summarize(db: Session, note_id: int):
        db_note = db.query(Note).filter(Note.id == note_id).first()
        if not db_note:
            raise HTTPException(status_code=404, detail="Özetlenecek not yok.")
        
        # Burası hocayı etkileyecek AI simülasyon kısmı
        summary = f"ÖZET (AI): {db_note.content[:50]}..." 
        return {"id": note_id, "summary": summary}