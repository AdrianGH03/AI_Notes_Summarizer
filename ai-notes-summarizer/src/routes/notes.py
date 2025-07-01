from fastapi import APIRouter, HTTPException, Form, Depends
from ..services.summarizer import summarize_and_keywords
from ..db.crud import save_jobad_summary, get_jobad_by_user_and_text
from ..db.connection import SessionLocal
from ..db.models import JobAd
from typing import Optional
from pydantic import BaseModel


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Take job ad text and summarize it, store it in Postgres, and return the summary to frontend
@router.post("/summarize")
async def summarize_notes(user_id: int = Form(...), text: Optional[str] = Form(None), company_name: Optional[str] = Form(None), db=Depends(get_db)):
    if not text:
        raise HTTPException(status_code=400, detail="Text is required for summarization")
    
    existing = get_jobad_by_user_and_text(db, user_id, text)
    if existing:
        return {
            "original_text": existing.original_text,
            "summarized_text": existing.summarized_text,
            "keywords": existing.keywords,
            "requirements": existing.requirements,
            "company_name": existing.company_name if existing.company_name else f"Company #{existing.id}",
            "message": "Duplicate detected. Returning existing summary."
        }
    
    try:
        result = summarize_and_keywords(text)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Summarization failed: {str(e)}")
    if not result:
        raise HTTPException(status_code=500, detail="Error in summarization process")
    
    summarized_text = save_jobad_summary(db, {
        "original_text": text,
        "user_id": user_id,
        "summarized_text": result.get("summary"),
        "keywords": ", ".join(result.get("keywords")), 
        "requirements": result.get("requirements"),
        "id": result.get("jobad_id", None),
        "company_name": company_name if company_name else None
    })
    return {
        "original_text": text,
        "summarized_text": summarized_text.summarized_text,
        "keywords": summarized_text.keywords,
        "requirements": summarized_text.requirements,
        "jobad_id": summarized_text.id,
        "company_name": summarized_text.company_name if summarized_text.company_name else f"Company #{summarized_text.id}",
    }

@router.get("/summaries-list/{user_id}")
async def get_summaries_list(user_id: int, db=Depends(get_db)):
    summaries = db.query(JobAd).filter(JobAd.user_id == user_id).all()
    if not summaries:
        raise HTTPException(status_code=404, detail="No summaries found for this user")
    
    return [
        {
            "id": job_ad.id,
            "original_text": job_ad.original_text,
            "summarized_text": job_ad.summarized_text,
            "company_name": job_ad.company_name if job_ad.company_name else f"Company #{job_ad.id}"
        }
        for job_ad in summaries
    ]


@router.delete("/delete/{jobad_id}/{user_id}")
async def delete_jobad(jobad_id: int, user_id: int, db=Depends(get_db)):
    jobad = db.query(JobAd).filter(JobAd.id == jobad_id, JobAd.user_id == user_id).first()
    if not jobad:
        raise HTTPException(status_code=404, detail="Job ad not found")
    
    db.delete(jobad)
    db.commit()
    return {"message": "Job ad deleted successfully"}
