from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict
from datetime import datetime


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
    ai_summary: Optional[str] = None
    
    class Config:
        from_attributes = True


class AnalysisRequest(BaseModel):
    """5 soruluk testten gelen cevapları (q1, q2, q3, q4, q5) sözlük yapısında alır."""
    answers: Dict[str, str] 

class AnalysisResponse(BaseModel):
    """Dashboard'daki beyin animasyonu ve grafikleri besleyen veriler."""
    brain_balance: str       
    memory_score: List[int]  
    recommendation: str      
    insight_text: str        


class CategoryStat(BaseModel):
    category: str
    count: int
    percentage: float

class NoteStatsResponse(BaseModel):
    """Analytics paneli için gereken tüm toplu veriler."""
    total_notes: int
    important_count: int
    category_distribution: List[CategoryStat]
    ai_insight: Optional[str] = "Henüz yeterli veri yok..."
    focus_alert: Optional[bool] = False


class NoteShareRequest(BaseModel):
    """EmailStr kullanarak geçersiz maillerin en baştan reddedilmesini sağlar."""
    email: EmailStr 

    class Config:
        from_attributes = True