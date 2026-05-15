from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.sql import func
from .database import Base

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    category = Column(String, default="General") 
    bg_color = Column(String, default="#ffffff") 
    is_important = Column(Boolean, default=False)
    importance_score = Column(Integer, default=0) 
    ai_summary = Column(String, nullable=True)
    # Yeni: Bu notun hangi bilişsel alanı tetiklediğini takip etmek için
    cognitive_tag = Column(String, nullable=True, default="Analytical") 
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class CognitiveProfile(Base):
    """
    Dashboard'daki 'Bilişsel Davranış Analizi' sonuçlarını saklar.
    image_6d8393.png'deki grafikleri ve image_6d8afa.png'deki önerileri kalıcı yapar.
    """
    __tablename__ = "cognitive_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    brain_balance = Column(String)  # 'Left-Brained (Analytical)' veya 'Right-Brained (Creative)'
    
    # Dashboard'daki 'Memory Insights' grafiği için skorlar
    retention_score = Column(Float, default=0.0)
    detail_score = Column(Float, default=0.0)
    speed_score = Column(Float, default=0.0)
    
    # AI Önerileri (image_6d8afa.png'deki tablo verileri)
    recommendation_text = Column(String) # Egzersiz ve Takviye önerisi
    scientific_insight = Column(String)  # Bilimsel dayanak (Rationale)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())