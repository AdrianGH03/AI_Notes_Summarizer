from fastapi import APIRouter, HTTPException, Form, Depends, UploadFile, File
from ..db.crud import save_resume, get_resume_by_user_and_name
from ..db.connection import SessionLocal
from ..aws.s3_handler import upload_fileobj, file_exists, download_file
from ..services.read_resume import extract_text_from_pdf, suggest_resume_improvements
from ..db.models import JobAd
import tempfile
import os

router = APIRouter()

MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB
ALLOWED_EXTENSIONS = {".pdf"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/resumes/{user_id}")
async def get_user_resumes(user_id: int, db=Depends(get_db)):
    from src.db.models import Resume
    resumes = db.query(Resume).filter(Resume.user_id == user_id).all()
    if not resumes:
        raise HTTPException(status_code=404, detail="No resumes found for this user.")
    return resumes

#Upload a resume to S3, validate it, and save metadata to Postgres
@router.post("/upload")
async def upload_resume(file: UploadFile = File(...), user_id: int = Form(...), resume_name: str = Form(...), db=Depends(get_db)):
    
    #Validate Resume 
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF and DOCX allowed.")

    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large. Max 2MB allowed.")

    existing_resume = get_resume_by_user_and_name(db, user_id, resume_name)
    if existing_resume:
        raise HTTPException(status_code=409, detail="Resume with this name already exists for this user.")

    s3_key = f"{user_id}/{resume_name}{ext}"
    if file_exists(s3_key):
        raise HTTPException(status_code=409, detail="Resume with this name already exists in storage.")


    #Upload to S3
    from io import BytesIO
    fileobj = BytesIO(contents)
    try:
        upload_fileobj(fileobj, s3_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file to S3: {str(e)}")

    #Save to DB
    save_resume(db, user_id, resume_name + ext, s3_key)

    return {"message": "Resume uploaded successfully"}



#Return suggestions for resume improvements based on job ad keywords and requirements
@router.post("/update_resume_keywords")
async def update_resume_keywords(user_id: int, resume_name: str, jobad_id: int, db=Depends(get_db)):
    resume = get_resume_by_user_and_name(db, user_id, resume_name)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    s3_key = resume.s3_key

    # Get job ad from database
    job_ad = db.query(JobAd).filter(JobAd.id == jobad_id).first()
    if not job_ad:
        raise HTTPException(status_code=404, detail="Job ad not found")

    if not job_ad.keywords or not job_ad.requirements:
        raise HTTPException(status_code=400, detail="Job ad is missing keywords or requirements")
    


    # Download the resume from S3 and store in temp file, then suggest improvements
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    tmp_path = tmp.name
    tmp.close()

    try:
        download_file(s3_key, tmp_path)
        resume_text = extract_text_from_pdf(tmp_path)
        resume_text = resume_text.strip().lower()
    finally:
        os.remove(tmp_path)

    suggestions = suggest_resume_improvements(
        resume_text=resume_text,
        job_keywords=job_ad.keywords.split(','),
        job_requirements=job_ad.requirements
    )

    return {
        "suggestions": suggestions,
        "original_resume": resume_text
    }


@router.put("/replace_resume_file")
async def replace_resume_file(user_id: int = Form(...), new_resume_name: str = Form(...), file: UploadFile = File(...), db=Depends(get_db)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF allowed.")

    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large. Max 2MB allowed.")

    #Find the user's most recent resume (or the only one)
    from sqlalchemy import desc
    from src.db.models import Resume
    resume = db.query(Resume).filter(Resume.user_id == user_id).order_by(desc(Resume.id)).first()
    if not resume:
        raise HTTPException(status_code=404, detail="No resume found for this user.")

    old_s3_key = resume.s3_key
    new_s3_key = f"{user_id}/{new_resume_name}{ext}"

    # Optional: Delete the old file from S3
    from ..aws.s3_handler import delete_file
    try:
        delete_file(old_s3_key)
    except Exception:
        pass  

    #Upload new file to S3
    from io import BytesIO
    fileobj = BytesIO(contents)
    try:
        upload_fileobj(fileobj, new_s3_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file to S3: {str(e)}")

    #Update DB record
    resume.resume_name = new_resume_name + ext
    resume.s3_key = new_s3_key
    db.commit()
    db.refresh(resume)

    return {"message": "Resume replaced successfully"}

@router.delete("/delete_resume")
async def delete_resume(user_id: int, resume_name: str, db=Depends(get_db)):
    resume = get_resume_by_user_and_name(db, user_id, resume_name)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    #Delete from S3
    try:
        from ..aws.s3_handler import delete_file
        delete_file(resume.s3_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file from S3: {str(e)}")

    #Delete from DB
    db.delete(resume)
    db.commit()

    return {"message": "Resume deleted successfully"}