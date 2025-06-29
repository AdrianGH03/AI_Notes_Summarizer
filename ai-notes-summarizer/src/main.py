from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.notes import router as notes_router
from .routes.auth import router as auth_router
from .routes.resume import router as resume_router
from src.db import models
from src.db.connection import engine

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notes_router, prefix="/notes")
app.include_router(auth_router, prefix="/auth")
app.include_router(resume_router, prefix="/resume")

#This creates the postgres tables, do not remove.
models.Base.metadata.create_all(bind=engine)