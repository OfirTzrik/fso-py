import logging

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from sqlalchemy.exc import OperationalError

from database import Base, engine
from middleware import database_unavailable, log_requests
from routers import notes

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

Base.metadata.create_all(engine)

app = FastAPI()

app.middleware("http")(log_requests)
app.add_exception_handler(OperationalError, database_unavailable)
app.include_router(notes.router)


@app.get("/", response_class=HTMLResponse)
def root() -> str:
	"""Handle get requests to the root of the website, sending
	HTML to be rendered instead of the usual JSON."""
	return "<h1>Hello World!</h1>"
