from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

# Create FastAPI app instance
app = FastAPI()

# Create all tables in the database using SQLAlchemy models
models.Base.metadata.create_all(bind=engine)

# Pydantic model for a choice, used for validation and serialization
class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool

# Pydantic model for a question, including a list of choices
class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]

# Dependency to provide a database session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db  # Provide the session to the path operation
    finally:
        db.close()  # Ensure the session is closed after the request

# Annotated type for dependency injection of the database session
db_dependency = Annotated[Session, Depends(get_db)]

# Endpoint to retrieve a question by its ID
@app.get("/questions/{question_id}")
async def read_question(question_id: int, db: db_dependency):
    # Query the database for the question with the given ID
    result = db.query(models.Questions).filter(models.Questions.id == question_id).first()
    if not result:
        # Raise a 404 error if the question is not found
        raise HTTPException(status_code=404, detail="Question not found")
    return result

# Endpoint to retrieve all choices for a specific question
@app.get("/choices/{question_id}")
async def read_choices(question_id: int, db: db_dependency):
    # Query the database for choices linked to the given question ID
    result = db.query(models.Choices).filter(models.Choices.question_id == question_id).all()
    if not result:
        # Raise a 404 error if no choices are found
        raise HTTPException(status_code=404, detail="Choices not found for this question")
    return result

# Endpoint to create a new question and its choices
@app.post("/questions/")
async def create_question(question: QuestionBase, db: db_dependency):
    # Create a new Questions row in the database
    db_question = models.Questions(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)  # Get the generated ID for the new question

    # Create Choices rows for each choice in the request, linked to the new question
    for choice in question.choices:
        db_choice = models.Choices(
            choice_text=choice.choice_text,
            is_correct=choice.is_correct,
            question_id=db_question.id
        )