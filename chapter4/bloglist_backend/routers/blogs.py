from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from schemas import BlogCreate, BlogOut, BlogUpdate
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


@router.delete("/{blog_id}", status_code=204)
def delete_blog(blog_id: int, db: Session = Depends(get_db)) -> None:
	blog = db.get(Blog, blog_id)
	if blog is not None:
		db.delete(blog)
		db.commit()


@router.patch("/{blog_id}")
def update_blog(blog_id: int, data: BlogUpdate, db: Session = Depends(get_db)) -> BlogOut:
	blog = db.get(Blog, blog_id)
	if blog is None:
		raise HTTPException(status_code=404, detail="blog not found")

	# exclude_unset drops fields the cliends didn't send
	# exclude_none drops fields the client sent as null
	for field, value in data.model_dump(exclude_unset=True, exclude_none=True).items():
		setattr(blog, field, value)
	db.commit()
	db.refresh(blog)

	# db.get gave us a Blog object, while Pydantic's model_validate
	# knows how to read dicts, so BlogOut's from_attributes tells
	# Pydantic to read it like an object instead.
	return BlogOut.model_validate(blog)
