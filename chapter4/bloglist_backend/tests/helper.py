from sqlalchemy import select

from database import SessionLocal
from models import Blog
from schemas import BlogOut

initial_blogs = [
	{"title": "Title1", "author": "Some Guy", "url": "http://google.com", "likes": 17},
	{"title": "Title2", "author": "Some Other Guy", "url": "http://wikipedia.com", "likes": 6},
	{"title": "Title3", "author": "Some Guy", "url": "http://youtube.com", "likes": 12},
]


def blogs_in_db() -> list[dict]:
	with SessionLocal() as db:
		blogs = db.scalars(select(Blog)).all()
		# Convert the BlogOut database object to BlogOut and then
		# to a dictionary
		return [BlogOut.model_validate(n).model_dump() for n in blogs]


def non_existing_id() -> int:
	with SessionLocal() as db:
		blog = Blog(title="abc", author="abc", url="abc", likes="123")
		db.add(blog)
		db.commit()
		blog_id = blog.id
		db.delete(blog)
		db.commit()
	return blog_id
