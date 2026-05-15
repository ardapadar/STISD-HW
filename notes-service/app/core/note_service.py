import requests
import logging
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db import models
from app.api import note_schema

logger = logging.getLogger("UYG414-Core")

def analyze_cognitive_activity(answers: dict):
    """
    Processes the 'Behavioral Profiling' from the English Dashboard.
    Returns scientific recommendations in English.
    """
    left_score = 0
    right_score = 0

    # 1. Task forgetting (English Q1)
    if answers.get("q1") == "Nadiren": left_score += 1
    else: right_score += 1

    # 2. Note style (English Q2)
    if answers.get("q2") == "Detaylı ve Uzun": left_score += 2
    else: right_score += 2

    # 3. Review frequency (English Q3)
    if answers.get("q3") == "Günlük": left_score += 1
    else: right_score += 1

    # 4. Stress response (English Q4)
    if answers.get("q4") == "Daha Düzenli Olur": left_score += 2
    else: right_score += 2

    # Determination of results (English output)
    if left_score >= right_score:
        target = "Left-Brained (Analytical)"
        rationale = "Your verbal and analytical data processing might need a boost."
        exercise = "Logic puzzles, Sudoku, or foreign language practice."
        supplement = "Vitamin B12 & Folic Acid: Critical for neurotransmitter synthesis."
    else:
        target = "Right-Brained (Creative)"
        rationale = "Visual-spatial and episodic memory areas could be stimulated."
        exercise = "Charcoal drawing, meditation, or creative visualization."
        supplement = "Omega-3 (DHA): Increases cell membrane flexibility and synaptic plasticity."

    return {
        "target_region": target,
        "scientific_rationale": rationale,
        "recommended_exercise": exercise,
        "supplement": supplement,
        "scores": {"left": left_score, "right": right_score}
    }

def analyze_note_with_ai(content: str):
    text = content.lower()
    # English categories for the English Dashboard
    categories = {
        "Academic": ["exam", "homework", "midterm", "final", "lesson", "school", "project"],
        "Professional": ["meeting", "mail", "presentation", "office", "client", "report"],
        "Urgent": ["urgent", "immediately", "attention", "doctor", "deadline"],
        "Personal": ["market", "maybe", "shopping", "food", "book", "home"]
    }
    
    found_category = "General"
    score = 0
    
    for cat, words in categories.items():
        if any(word in text for word in words):
            found_category = cat
            if cat == "Urgent": score = 95
            elif cat == "Academic": score = 85
            elif cat == "Professional": score = 75
            else: score = 40
            break

    ai_report = f"[{found_category}] Focused: {content[:30]}..." if len(content) > 30 else f"{found_category}: {content}"
    is_imp_ai = score >= 75
    return is_imp_ai, score, ai_report, found_category

def create_new_note(db: Session, note: note_schema.NoteCreate):
    # Perform AI analysis on the content
    is_imp_ai, score, summary, ai_cat = analyze_note_with_ai(note.content)
    
    db_note = models.Note(
        title=note.title,
        content=note.content,
        category=note.category if note.category != "General" else ai_cat,
        bg_color=note.bg_color,
        is_important=note.is_important or is_imp_ai, 
        importance_score=score,
        ai_summary=summary,
        cognitive_tag="Analytical" if score > 50 else "Creative"
    )
    
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    
    logger.info(f"New Thought Archived: {note.title}")
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