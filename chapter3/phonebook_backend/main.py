import time

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from datetime import datetime
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError

from database import get_db, Base, engine
from models import Person
from schemas import PersonCreate, PersonUpdate, PersonOut

Base.metadata.create_all(engine)

app = FastAPI()

@app.get("/api/persons")
def get_persons(db: Session = Depends(get_db)) -> list[PersonOut]:
	persons = db.scalars(select(Person)).all()
	return [PersonOut.model_validate(person) for person in persons]

@app.get("/info", response_class=HTMLResponse)
def get_info(db: Session = Depends(get_db)) -> str:
	num_phonebook = db.scalar(select(func.count()).select_from(Person))
	current = datetime.now()
	return f"<p>Phonebook has info for {num_phonebook} people</p>" \
		f"<p>{current}</p>"

@app.get("/api/persons/{id}")
def get_person(id: int, db: Session = Depends(get_db)) -> PersonOut:
	person = db.get(Person, id)
	if person is None:
		raise HTTPException(status_code=404, detail="person not found")
	return PersonOut.model_validate(person)

@app.delete("/api/persons/{id}", status_code=204)
def delete_person(id: int, db: Session = Depends(get_db)) -> None:
	person = db.get(Person, id)
	if person is not None:
		db.delete(person)
		db.commit()

@app.post("/api/persons", status_code=201)
def create_person(person: PersonCreate, db: Session = Depends(get_db)) -> PersonOut:
	new_person = Person(name=person.name, number=person.number)
	dup = db.scalar(select(Person).where(Person.name == person.name))
	if dup is not None:
		raise HTTPException(status_code=400, detail="name must be unique")
	db.add(new_person)
	db.commit()
	db.refresh(new_person)
	return PersonOut.model_validate(new_person)

@app.patch("/api/persons/{id}")
def update_person(id: int, updated_person: PersonUpdate, db: Session = Depends(get_db)) -> PersonOut:
	person = db.get(Person, id)
	if person is None:
		raise HTTPException(status_code=404, detail="person not found")
	for field, value in updated_person.model_dump(exclude_unset=True).items():
		setattr(person, field, value)
	db.commit()
	db.refresh(person)
	return PersonOut.model_validate(person)

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

@app.exception_handler(OperationalError)
def database_unavailable(request, exc):
	print("database error", exc.orig)
	return JSONResponse(status_code=503, content={"detail": "database unavailable"})