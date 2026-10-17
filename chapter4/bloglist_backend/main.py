import logging

from fastapi import FastAPI

from database import engine, Base
from middleware import log_requests
from routers import blogs

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

Base.metadata.create_all(engine)

app = FastAPI()

app.middleware("http")(log_requests)
app.include_router(blogs.router)
