from fastapi import Depends, APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from schemas import BlogCreate, BlogOut
from models import Blog

router = APIRouter(prefix="/api/blogs")


@router.get("")
def get_blogs(db: Session = Depends(get_db)) -> list[BlogOut]:
	blogs = db.scalars(select(Blog)).all()
	return [BlogOut.model_validate(b) for b in blogs]


@router.post("", status_code=201)
def create_blog(data: BlogCreate, db: Session = Depends(get_db)) -> BlogOut:
	blog = Blog(title=data.title, author=data.author, url=data.url, likes=data.likes)
	db.add(blog)
	db.commit()
	db.refresh(blog)
	return BlogOut.model_validate(blog)
