from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base

# Define the Questions table/model
class Questions(Base):
    __tablename__ = "questions"  # Table name in the database

    id = Column(Integer, primary_key=True, index=True)  # Unique ID for each question
    question_text = Column(String, index=True)          # The text of the question

# Define the Choices table/model
class Choices(Base):
    __tablename__ = "choices"  # Table name in the database

    id = Column(Integer, primary_key=True, index=True)              # Unique ID for each choice
    choice_text = Column(String, index=True)                        # The text of the choice
    is_correct = Column(Boolean, default=False)                     # Whether this choice is correct
    question_id = Column(Integer, ForeignKey("questions.id"))       # Link to the related question