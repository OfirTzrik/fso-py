from sqlalchemy import select

from database import SessionLocal
from models import Note
from schemas import NoteOut

initial_notes = [
	{"content": "HTML is easy", "important": False},
	{"content": "Browser can execute only JavaScript", "important": True},
]


def notes_in_db() -> list[dict]:
	with SessionLocal() as db:
		notes = db.scalars(select(Note)).all()
		return [NoteOut.model_validate(n).model_dump() for n in notes]


def non_existing_id() -> int:
	with SessionLocal() as db:
		note = Note(content="willremovethissoon")
		db.add(note)
		db.commit()
		note_id = note.id
		db.delete(note)
		db.commit()
	return note_id
