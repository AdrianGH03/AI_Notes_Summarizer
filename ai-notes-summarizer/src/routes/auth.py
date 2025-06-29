from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.connection import SessionLocal
from src.db.crud import get_user_by_email, create_user, update_user_resume_name
from src.db.models import User
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class UserAuth(BaseModel):
    email: str
    resume_name: Optional[str] = None

class UserOut(BaseModel):
    id: int
    email: str
    resume_name: Optional[str] = None

    class Config:
        orm_mode = True

class ResumeNameUpdate(BaseModel):
    id: int
    resume_name: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup", response_model=UserOut)
def signup(user: UserAuth, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    return create_user(db, user.email, user.resume_name)

@router.post("/login", response_model=UserOut)
def login(user: UserAuth, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user.email)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    return existing_user

