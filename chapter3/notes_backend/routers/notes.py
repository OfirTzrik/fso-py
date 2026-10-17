from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import Note
from schemas import NoteCreate, NoteOut, NoteUpdate

# Registers the router to /api/notes/ as the root so the REST API
# listens on that and only need to specify paths under it.
router = APIRouter(prefix="/api/notes")


# db: Session = Depends(get_db) means that this route needs a db
# to work and it can get it by calling get_db (which yields to give
# back control toe this function)
@router.get("")
def get_notes(db: Session = Depends(get_db)) -> list[NoteOut]:
	"""Get a list of all Note objects. FastAPI sends it as a JSON."""
	notes = db.scalars(select(Note)).all()
	# Return all notes after validating the structure of each one

	return [NoteOut.model_validate(n) for n in notes]


@router.get("/{note_id}")
def get_note(note_id: int, db: Session = Depends(get_db)) -> NoteOut:
	"""Get the note with the requested id and return it.
	If it was not found (None) return the 404 status code."""
	note = db.get(Note, note_id)
	if note is None:
		raise HTTPException(status_code=404, detail="note not found")

	return NoteOut.model_validate(note)


@router.delete("/{note_id}", status_code=204)
def delete_note(note_id: int, db: Session = Depends(get_db)) -> None:
	"""Delete a note with id by updating the global list of
	notes without including it and respond with an empty
	response body (code 204)."""
	note = db.get(Note, note_id)
	if note is not None:
		db.delete(note)
		db.commit()


@router.post("", status_code=201)
def create_note(data: NoteCreate, db: Session = Depends(get_db)) -> NoteOut:
	"""Add a new note based on what the user provided and
	report it was created (code 201)"""
	note = Note(content=data.content, important=data.important)
	# Add a new note to the database and register the changes
	db.add(note)
	db.commit()
	# Reloads the object from the database which fills in values
	# the database created such as the new id.
	db.refresh(note)
	return NoteOut.model_validate(note)


@router.patch("/{note_id}")
def update_note(note_id: int, data: NoteUpdate, db: Session = Depends(get_db)) -> NoteOut:
	"""Update only the specified fields of a note"""
	note = db.get(Note, note_id)
	if note is None:
		raise HTTPException(status_code=404, detail="note not found")

	# exclude_unset drops fields the cliends didn't send
	# exclude_none drops fields the client sent as null
	for field, value in data.model_dump(exclude_unset=True, exclude_none=True).items():
		setattr(note, field, value)
	db.commit()
	db.refresh(note)

	# db.get gave us a Note object, while Pydantic's model_validate
	# knows how to read dicts, so NoteOut's from_attributes tells
	# Pydantic to read it like an object instead.
	return NoteOut.model_validate(note)
