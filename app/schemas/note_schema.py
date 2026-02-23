from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Temel Not şeması
class NoteBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, example="Toplantı Notu")
    content: str = Field(..., min_length=1, example="Bugün mikroservisler hakkında konuştuk.")

# Not oluştururken beklediğimiz veri
class NoteCreate(NoteBase):
    pass

# Not güncellerken (Her alan opsiyonel - Partial Update için kritik!)
class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

# API'den kullanıcıya dönecek veri (Şifre vb. olsa burada gizlerdik)
class NoteResponse(NoteBase):
    id: int
    created_at: datetime

    class ConfigDict:
        from_attributes = True # SQLAlchemy modellerini Pydantic'e dönüştürmek için