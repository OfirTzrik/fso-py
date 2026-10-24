import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete

from database import SessionLocal
from main import app
from models import Note
from tests.helper import initial_notes, non_existing_id, notes_in_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_notes():
	with SessionLocal() as db:
		db.execute(delete(Note))
		db.add_all([Note(**n) for n in initial_notes])
		db.commit()


class TestGetAllNotes:
	def test_notes_are_returned_as_json(self):
		response = client.get("/api/notes")
		assert response.status_code == 200
		assert response.headers["content-type"] == "application/json"

	def test_all_notes_are_returned(self):
		response = client.get("/api/notes")
		assert len(response.json()) == len(initial_notes)

	def test_a_specific_note_is_among_the_returned_notes(self):
		response = client.get("/api/notes")
		contents = [n["content"] for n in response.json()]
		assert "HTML is easy" in contents


class TestGetOneNote:
	def test_succeeds_with_a_valid_id(self):
		note_to_view = notes_in_db()[0]
		response = client.get(f"/api/notes/{note_to_view['id']}")
		assert response.status_code == 200
		assert response.json() == note_to_view

	def test_fails_with_404_if_note_does_not_exist(self):
		response = client.get(f"/api/notes/{non_existing_id()}")
		assert response.status_code == 404

	def test_fails_with_422_if_id_is_invalid(self):
		response = client.get("/api/notes/abc")
		assert response.status_code == 422


class TestAddNote:
	def test_succeeds_with_valid_data(self):
		new_note = {"content": "pytest makes testing easy", "important": True}
		response = client.post("/api/notes", json=new_note)
		assert response.status_code == 201

		notes_at_end = notes_in_db()
		assert len(notes_at_end) == len(initial_notes) + 1
		assert "pytest makes testing easy" in [n["content"] for n in notes_at_end]

	def test_fails_with_422_if_content_is_missing(self):
		response = client.post("/api/notes", json={"important": True})
		assert response.status_code == 422
		assert len(notes_in_db()) == len(initial_notes)


class TestDeleteNote:
	def test_succeeds_with_204_if_id_is_valid(self):
		note_to_delete = notes_in_db()[0]
		response = client.delete(f"/api/notes/{note_to_delete['id']}")
		assert response.status_code == 204

		notes_at_end = notes_in_db()
		assert len(notes_at_end) == len(initial_notes) - 1
		assert note_to_delete not in notes_at_end
