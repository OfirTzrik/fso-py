import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete

from database import SessionLocal
from main import app
from models import Blog
from tests.helper import initial_blogs, non_existing_id, blogs_in_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_blogs():
	with SessionLocal() as db:
		db.execute(delete(Blog))
		db.add_all([Blog(**n) for n in initial_blogs])
		db.commit()


class TestGetAllBlogs:
	def test_all_blogs_are_returned(self):
		response = client.get("/api/blogs")
		assert response.status_code == 200
		assert len(response.json()) == len(initial_blogs)

	def test_all_blogs_have_id(self):
		response = blogs_in_db()
		for blog in response:
			assert "id" in blog


class TestNewCreatedBlogs:
	def test_create_new_blog(self):
		response = client.post(
			"/api/blogs",
			json={
				"title": "Something Cool",
				"author": "Jeff",
				"url": "http://wikipedia.com",
				"likes": 99,
			},
		)

		blogs_at_end = blogs_in_db()

		assert response.status_code == 201
		assert len(blogs_at_end) == len(initial_blogs) + 1
		assert "Something Cool" in [blog["title"] for blog in blogs_at_end]

	def test_new_blog_no_likes_has_zero(self):
		response = client.post(
			"/api/blogs",
			json={
				"title": "Something Cool",
				"author": "Jeff",
				"url": "http://wikipedia.com",
			},
		)

		added_blog = next(b for b in blogs_in_db() if b["id"] == response.json()["id"])

		assert response.status_code == 201
		assert response.json()["likes"] == 0
		assert added_blog["likes"] == 0

	def test_blog_without_title_or_url_rejected(self):
		# Missing title
		response = client.post(
			"/api/blogs",
			json={
				"author": "Jeff",
				"url": "http://wikipedia.com",
				"likes": 99,
			},
		)

		assert response.status_code == 422
		assert len(blogs_in_db()) == len(initial_blogs)

		# Missing URL
		response = client.post(
			"/api/blogs",
			json={
				"title": "Something Cool",
				"author": "Jeff",
				"likes": 99,
			},
		)

		assert response.status_code == 422
		assert len(blogs_in_db()) == len(initial_blogs)


class TestDeleteBlog:
	def test_delete_blog(self):
		blog_to_delete = blogs_in_db()[0]
		response = client.delete(f"/api/blogs/{blog_to_delete['id']}")

		assert response.status_code == 204
		assert len(blogs_in_db()) == len(initial_blogs) - 1


class TestUpdateBlog:
	def test_patch_blog(self):
		blog_to_update = blogs_in_db()[0]
		response = client.patch(f"/api/blogs/{blog_to_update['id']}", json={"likes": 54})

		# After the update the blog seems to move to the end of the database
		# In order to not rely on it, get the blog by its ids intead of [-1]
		blog_after_update = next(b for b in blogs_in_db() if b["id"] == blog_to_update["id"])

		assert response.status_code == 200
		assert response.json()["likes"] == 54
		assert blog_after_update["likes"] == 54

	def test_patch_missing_id(self):
		response = client.patch(f"/api/blogs/{non_existing_id()}", json={"likes": 54})

		assert response.status_code == 404

	def test_patch_no_likes(self):
		response = client.patch(f"/api/blogs/{non_existing_id()}", json={})

		assert response.status_code == 422
