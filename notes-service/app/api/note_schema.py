from pydantic import BaseModel
from typing import Optional

class NoteBase(BaseModel):
    title: str
    content: str
    category: Optional[str] = "General"
    bg_color: Optional[str] = "#ffffff"
    is_important: bool = False

class NoteCreate(NoteBase):
    
    pass

class NoteResponse(NoteBase):
    id: int
    ai_summary: Optional[str]
    
    class Config:
        from_attributes = True 