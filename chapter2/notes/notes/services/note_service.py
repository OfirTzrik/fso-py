''' In this file we put the functions for everything the server
can do with Note objects (the services offered), other files
(such as notes.py) will only make use of the provided services
and not provide them directly to keep things organized '''

import httpx
import os

from ..models import Note

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:3001")
BASE_URL = f"{BACKEND_URL}/api/notes"

# Get all notes
async def get_all() -> list[Note]:
	async with httpx.AsyncClient() as client:
		response = await client.get(BASE_URL)
	response.raise_for_status()
	return [Note(**n) for n in response.json()]

# Create a new note
async def create(content: str, important: bool) -> Note:
	async with httpx.AsyncClient() as client:
		response = await client.post(BASE_URL, json={"content": content, "important": important})
	response.raise_for_status()
	return Note(**response.json())

# Update the 'important' field of a specific note
async def update_important(note_id: int, important: bool) -> Note:
	async with httpx.AsyncClient() as client:
		response = await client.patch(f"{BASE_URL}/{note_id}", json={"important": important})
	response.raise_for_status()
	return Note(**response.json())