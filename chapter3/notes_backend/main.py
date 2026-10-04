import time

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

# Model for how FastAPI stores the data
class Note(BaseModel):
	id: str
	content: str
	important: bool

# A separate model for what the client sends (The user does
# not choose the note's id). Also put a limitation and default
# value for Pydantic to follow.
# Separate models for the input and output.
class NoteCreate(BaseModel):
	content: str = Field(min_length=1)
	important: bool = False

notes: list[Note] = [
	Note(id="1", content="HTML is easy", important=True),
	Note(id="2", content="Browser can execute only JavaScript", important=False),
	Note(id="3", content="GET and POST are the most important methods of the HTTP protocol", important=True)
]

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def root() -> str:
	'''Handle get requests to the root of the website, sending
	HTML to be rendered instead of the usual JSON.'''
	return "<h1>Hello World!</h1>"

@app.get("/api/notes")
def get_notes() -> list[Note]:
	'''Get a list of all Note objects. FastAPI sends it as a JSON.'''
	return notes

@app.get("/api/notes/{note_id}")
def get_note(note_id: str) -> Note:
	'''Get the note with the requested id and return it.
	If it was not found (None) return the 404 status code.'''
	note = next((n for n in notes if n.id == note_id), None)
	if note is None:
		raise HTTPException(status_code=404, detail="note not found")
	return note

@app.delete("/api/notes/{note_id}", status_code=204)
def delete_note(note_id: str) -> None:
	'''Delete a note with id by updating the global list of
	notes without including it and respond with an empty
	response body (code 204).'''
	global notes
	notes = [n for n in notes if n.id != note_id]

def generate_id() -> str:
	max_id = max((int(n.id) for n in notes), default=0) # default=0 for an empty list
	return str(max_id + 1)

@app.post("/api/notes", status_code=201)
def create_note(note: NoteCreate) -> Note:
	'''Add a new note based on what the user provided and
	report it was created (code 201)'''
	new_note = Note(id=generate_id(), content=note.content, important=note.important)
	notes.append(new_note)
	return new_note

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