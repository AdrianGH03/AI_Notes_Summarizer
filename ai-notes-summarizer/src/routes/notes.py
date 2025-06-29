from fastapi import APIRouter, HTTPException, Form, Depends
from ..services.summarizer import summarize_and_keywords
from ..db.crud import save_jobad_summary, get_jobad_by_user_and_text
from ..db.connection import SessionLocal
from typing import Optional
from pydantic import BaseModel


router = APIRouter()

class JobAd(BaseModel):
    original_text: str
    user_id: int
    summarized_text: Optional[str] = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Take job ad text and summarize it, store it in Postgres, and return the summary to frontend
@router.post("/summarize")
async def summarize_notes(user_id: int = Form(...), text: Optional[str] = Form(None), db=Depends(get_db)):
    if not text:
        raise HTTPException(status_code=400, detail="Text is required for summarization")
    
    existing = get_jobad_by_user_and_text(db, user_id, text)
    if existing:
        return {
            "original_text": existing.original_text,
            "summarized_text": existing.summarized_text,
            "keywords": existing.keywords,
            "requirements": existing.requirements,
            "message": "Duplicate detected. Returning existing summary."
        }
    
    result = summarize_and_keywords(text)
    if not result:
        raise HTTPException(status_code=500, detail="Error in summarization process")
    
    summarized_text = save_jobad_summary(db, {
        "original_text": text,
        "user_id": user_id,
        "summarized_text": result.get("summary"),
        "keywords": ", ".join(result.get("keywords")), 
        "requirements": result.get("requirements"),
        "id": result.get("jobad_id", None) 
    })
    return {
        "original_text": text,
        "summarized_text": summarized_text.summarized_text,
        "keywords": summarized_text.keywords,
        "requirements": summarized_text.requirements,
        "jobad_id": summarized_text.id,
    }

