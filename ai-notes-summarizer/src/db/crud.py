from typing import Optional
from sqlalchemy.orm import Session
from src.db.models import User
from src.db.models import JobAd

#CRUD operations for User model
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, email: str, resume_name: Optional[str] = None):
    user = User(email=email, resume_name=resume_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def update_user_resume_name(db: Session, user_id: int, resume_name: str):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.resume_name = resume_name
        db.commit()
        db.refresh(user)
    return user


#CRUD operations for Resume model
def save_resume(db: Session, user_id: int, resume_name: str, s3_key: str):
    from src.db.models import Resume
    new_resume = Resume(user_id=user_id, resume_name=resume_name, s3_key=s3_key)
    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)
    return new_resume

def get_resume_by_user_and_name(db: Session, user_id: int, resume_name: str):
    from src.db.models import Resume
    return db.query(Resume).filter(Resume.user_id == user_id, Resume.resume_name == resume_name).first()


#CRUD operations for JobAd model
def save_jobad_summary(db: Session, job_ad: dict):
    from src.db.models import JobAd
    new_job_ad = JobAd(
        original_text=job_ad['original_text'],
        user_id=job_ad['user_id'],
        summarized_text=job_ad.get('summarized_text'),
        keywords=job_ad.get('keywords'),
        requirements=job_ad.get('requirements'),
        company_name=job_ad.get('company_name')
    )
    db.add(new_job_ad)
    db.commit()
    db.refresh(new_job_ad)
    return new_job_ad

def get_jobad_by_user_and_text(db: Session, user_id: int, original_text: str):
    return db.query(JobAd).filter(JobAd.user_id == user_id, JobAd.original_text == original_text).first()

def get_jobad_by_company_and_text(db: Session, company_name: str, original_text: str):
    return db.query(JobAd).filter(JobAd.company_name == company_name, JobAd.original_text == original_text).first()
