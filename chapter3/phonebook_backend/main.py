import time

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from datetime import datetime
from secrets import SystemRandom

class Person(BaseModel):
	id: str
	name: str
	number: str

class CreatePerson(BaseModel):
	name: str = Field(min_length=1)
	number: str = Field(min_length=1)

phonebook: list[Person] = [
	Person(id="1", name="Maren Holt", number="040-123456"),
	Person(id="2", name="Idris Okafor", number="39-44-5323523"),
	Person(id="3", name="Lena Vasquez", number="12-43-234345"),
	Person(id="4", name="Tobias Rhee", number="39-23-6423122"),
]

app = FastAPI()

@app.get("/api/persons")
def get_persons() -> list[Person]:
	return phonebook

@app.get("/info", response_class=HTMLResponse)
def get_info() -> str:
	current = datetime.now()
	return f"<p>Phonebook has info for {len(phonebook)} people</p>" \
		f"<p>{current}</p>"

@app.get("/api/persons/{id}")
def get_person(id: str) -> Person:
	person = next((p for p in phonebook if p.id == id), None)
	if person is None:
		raise HTTPException(status_code=404, detail="person not found")
	return person

@app.delete("/api/persons/{id}", status_code=204)
def delete_person(id: str) -> None:
	global phonebook
	phonebook = [p for p in phonebook if p.id != id]

def generate_id() -> str:
	random_generator = SystemRandom()
	return str(random_generator.randrange(start=0, stop=1000000))

@app.post("/api/persons", status_code=201)
def create_person(person: CreatePerson) -> Person:
	new_person = Person(id=generate_id(), name=person.name, number=person.number)
	dup = [p.name for p in phonebook if p.name == new_person.name]
	if dup:
		raise HTTPException(status_code=400, detail="name must be unique")
	phonebook.append(new_person)
	return new_person

@app.middleware("http")
async def log_request(request: Request, call_next):
	start = time.perf_counter()
	# HTTP request arrives in parts so need to await for
	# the body to arrive. The Request object calls the
	# middleware as soon as the headers are in and in that
	# time it is possible the body has no yet arrived.
	body = await request.body()
	response = await call_next(request)
	ms = (time.perf_counter() - start) * 1000
	if request.method == "POST":
		print(request.method, request.url.path, response.status_code, f"{ms:.1f} ms", body.decode())
	else:
		print(request.method, request.url.path, response.status_code, f"{ms:.1f} ms")
	return response