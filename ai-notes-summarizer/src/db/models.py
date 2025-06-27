from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text)
    summary = Column(Text)

class NoteIn(BaseModel):
    text: str

class NoteOut(NoteIn):
    id: int
    summary: str