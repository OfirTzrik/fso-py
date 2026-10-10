import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv() # Load all environment variables from .env into os.environ
# If environment variables are supplied in a different way (for example
# through Render) than dotenv doesn't override them.

DATABASE_URL = os.environ["DATABASE_URL"]

# The object the access the database.
# It creates a connection pool to keep a few reusable connections open
# instead of opening new ones from scratch (slow process).
# pool_pre_ping sends a small query to check if the connection is dead
# before attempting to reuse (otherwise it can get a dead connection -
# for example in Neon as it is suspended after 5 minutes), if it is dead
# replace with a fresh connection.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
	pass

def get_db():
	db = SessionLocal()
	try:
		yield db # yield and not return so it can be closed later through the 'finally' block
	finally:
		db.close()
