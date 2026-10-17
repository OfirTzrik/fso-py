import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from pydantic import BaseModel, ConfigDict
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

load_dotenv()

engine = create_engine(os.environ["DATABASE_URL"], pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
	pass


class Blog(Base):
	__tablename__ = "blogs"

	id: Mapped[int] = mapped_column(primary_key=True)
	title: Mapped[str]
	author: Mapped[str]
	url: Mapped[str]
	likes: Mapped[int] = mapped_column(default=0)


class BlogCreate(BaseModel):
	title: str
	author: str
	url: str
	likes: int = 0


class BlogOut(BaseModel):
	model_config = ConfigDict(from_attributes=True)
	id: int
	title: str
	author: str
	url: str
	likes: int


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


Base.metadata.create_all(engine)

app = FastAPI()


@app.get("/api/blogs")
def get_blogs(db: Session = Depends(get_db)) -> list[BlogOut]:
	blogs = db.scalars(select(Blog)).all()
	return [BlogOut.model_validate(b) for b in blogs]


@app.post("/api/blogs", status_code=201)
def create_blog(data: BlogCreate, db: Session = Depends(get_db)) -> BlogOut:
	blog = Blog(title=data.title, author=data.author, url=data.url, likes=data.likes)
	db.add(blog)
	db.commit()
	db.refresh(blog)
	return BlogOut.model_validate(blog)
