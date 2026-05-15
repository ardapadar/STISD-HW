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
    # Yeni: Notun hangi bilişsel lobla ilgili olduğunu frontend'e bildirir
    cognitive_tag: Optional[str] = "Analytical" 
    created_at: datetime
    
    class Config:
        from_attributes = True

class AnalysisRequest(BaseModel):
    """Dashboard'daki 4 ana sorudan gelen cevapları alır (image_6d8393.png)."""
    answers: Dict[str, str] 

class AnalysisResponse(BaseModel):
    """
    Dashboard'daki beyin animasyonu, Memory Insights grafiği ve 
    bilimsel öneri tablosunu besler (image_6d8afa.png).
    """
    brain_balance: str        # Örn: 'Right-Brained (Personal)'
    memory_score: List[int]   # [Retention, Detail, Speed]
    recommendation: str       # Egzersiz ve Takviye birleşimi
    insight_text: str         # Scientific Rationale

class CognitiveProfileResponse(BaseModel):
    """Kullanıcının geçmiş analiz sonuçlarını listeleyebilmesi için."""
    id: int
    brain_balance: str
    retention_score: float
    detail_score: float
    speed_score: float
    recommendation_text: str
    scientific_insight: str
    created_at: datetime

    class Config:
        from_attributes = True

class CategoryStat(BaseModel):
    category: str
    count: int
    percentage: float

class NoteStatsResponse(BaseModel):
    total_notes: int
    important_count: int
    category_distribution: List[CategoryStat]
    ai_insight: Optional[str] = "Henüz yeterly veri yok..."
    focus_alert: Optional[bool] = False

class NoteShareRequest(BaseModel):
    email: EmailStr 

    class Config:
        from_attributes = True