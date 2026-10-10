import time

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError

from database import Base, engine, get_db
from models import Note
from schemas import NoteCreate, NoteOut, NoteUpdate

Base.metadata.create_all(engine)

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def root() -> str:
	'''Handle get requests to the root of the website, sending
	HTML to be rendered instead of the usual JSON.'''
	return "<h1>Hello World!</h1>"

# db: Session = Depends(get_db) means that this route needs a db
# to work and it can get it by calling get_db (which yields to give
# back control toe this function)
@app.get("/api/notes")
def get_notes(db: Session = Depends(get_db)) -> list[NoteOut]:
	'''Get a list of all Note objects. FastAPI sends it as a JSON.'''
	notes = db.scalars(select(Note)).all()
	# Return all notes after validating the structure of each one
	return [NoteOut.model_validate(n) for n in notes]

@app.get("/api/notes/{note_id}")
def get_note(note_id: int, db: Session = Depends(get_db)) -> NoteOut:
	'''Get the note with the requested id and return it.
	If it was not found (None) return the 404 status code.'''
	note = db.get(Note, note_id)
	if note is None:
		raise HTTPException(status_code=404, detail="note not found")
	return NoteOut.model_validate(note)

@app.delete("/api/notes/{note_id}", status_code=204)
def delete_note(note_id: int, db: Session = Depends(get_db)) -> None:
	'''Delete a note with id by updating the global list of
	notes without including it and respond with an empty
	response body (code 204).'''
	note = db.get(Note, note_id)
	if note is not None:
		db.delete(note)
		db.commit()

@app.post("/api/notes", status_code=201)
def create_note(data: NoteCreate, db: Session = Depends(get_db)) -> NoteOut:
	'''Add a new note based on what the user provided and
	report it was created (code 201)'''
	note = Note(content=data.content, important=data.important)
	# Add a new note to the database and register the changes
	db.add(note)
	db.commit()
	# Reloads the object from the database which fills in values
	# the database created such as the new id.
	db.refresh(note)
	return NoteOut.model_validate(note)

@app.patch("/api/notes/{note_id}")
def update_note(note_id: int, data: NoteUpdate, db: Session = Depends(get_db)) -> NoteOut:
	note = db.get(Note, note_id)
	if note is None:
		raise HTTPException(status_code=404, detail="note not found")
	for field, value in data.model_dump(exclude_unset=True).items():
		setattr(note, field, value)
	db.commit()
	db.refresh(note)
	return NoteOut.model_validate(note)

# A "middleware" is a function that works with every request
# before it is processed by any specific path operation. And also
# with every response before returning it.
# Middleware should be used for things that apply to all requests,
# such as logging, timing, etc.
@app.middleware("http")
async def log_requests(request: Request, call_next):
	'''Log the request and response time'''
	start = time.perf_counter()
	# Code before runs before the matching route
	response = await call_next(request)
	# Code after runs after the matching route
	ms = (time.perf_counter() - start) * 1000
	print(request.method, request.url.path, response.status_code, f"{ms:.1f} ms")
	return response

# OperationalError is raised whenever SQLAlchemy can't reach the
# database or the connection break
@app.exception_handler(OperationalError)
def database_unavailable(request, exc):
	'''Database unreachable or connection broke, return "503
	Service Unavailable" with a readable message instead of
	the generic "500 Internal Server Error"'''
	print("database error:", exc.orig)
	# JSON Response builds a response by hand
	return JSONResponse(status_code=503, content={"detail": "database unavailable"})