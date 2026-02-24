from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api import note_schema
from app.core import note_service

router = APIRouter()

@router.get("/", response_model=list[note_schema.NoteResponse])
def get_notes(db: Session = Depends(get_db)):
    return note_service.list_notes(db)

@router.post("/", response_model=note_schema.NoteResponse)
def create_note(note: note_schema.NoteCreate, db: Session = Depends(get_db)):
    return note_service.create_new_note(db, note)

@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    if not note_service.delete_note(db, note_id):
        raise HTTPException(status_code=404, detail="Not bulunamadı")
    return {"status": "success"}