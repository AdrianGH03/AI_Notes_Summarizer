from fastapi import APIRouter, HTTPException
from services.summarizer import summarize_text
from db.crud import save_note, get_notes
from db.models import NoteIn, NoteOut

router = APIRouter()

@router.post("/", response_model=NoteOut)
def create_note(note: NoteIn):
    summary = summarize_text(note.text)
    return save_note(note.text, summary)

@router.get("/", response_model=list[NoteOut])
def list_notes():
    return get_notes()