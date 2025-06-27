from .connection import SessionLocal
from .models import Note, NoteOut


def save_note(text: str, summary: str) -> NoteOut:
    session = SessionLocal()
    note = Note(text=text, summary=summary)
    session.add(note)
    session.commit()
    session.refresh(note)
    session.close()
    return NoteOut(id=note.id, text=note.text, summary=note.summary)


def get_notes() -> list[NoteOut]:
    session = SessionLocal()
    notes = session.query(Note).all()
    session.close()
    return [NoteOut(id=n.id, text=n.text, summary=n.summary) for n in notes]