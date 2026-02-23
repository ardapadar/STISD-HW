from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.note_schema import NoteCreate, NoteUpdate, NoteResponse
from app.services.note_service import NoteService # Yeni oluşturduğun servisi içe aktar

router = APIRouter()

@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    return NoteService.create(db, note)

@router.get("/", response_model=List[NoteResponse])
def get_notes(db: Session = Depends(get_db)):
    return NoteService.get_all(db)

# Diğer endpoint'leri de (Update, Delete, Summarize) benzer şekilde buraya ekle...

@router.put("/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, note: NoteUpdate, db: Session = Depends(get_db)):
    return NoteService.update(db, note_id, note)

@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    return NoteService.delete(db, note_id)

@router.get("/{note_id}/summarize")
def summarize_note(note_id: int, db: Session = Depends(get_db)):
    return NoteService.ai_summarize(db, note_id)