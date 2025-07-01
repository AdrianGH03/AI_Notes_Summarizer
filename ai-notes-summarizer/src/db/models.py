from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
#Models for the application
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    resume_name = Column(String, nullable=True)

class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    resume_name = Column(String)
    s3_key = Column(String, unique=True, nullable=False)

class JobAd(Base):
    __tablename__ = "job_ads"
    id = Column(Integer, primary_key=True, index=True)
    original_text = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    summarized_text = Column(Text, nullable=True)
    keywords = Column(Text, nullable=True)
    requirements = Column(Text, nullable=True)
    company_name = Column(String, nullable=True)
    


