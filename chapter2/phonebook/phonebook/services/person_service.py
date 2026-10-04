import httpx
import os

from ..models import Person

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:3001")
BASE_URL = f"{BACKEND_URL}/api/persons"

async def get_persons() -> list[Person]:
	'''Get all persons from the server'''
	async with httpx.AsyncClient() as client:
		response = await client.get(BASE_URL)
	response.raise_for_status()
	return [Person(**person) for person in response.json()]

async def create_person(name: str, number: str) -> Person:
	'''Create a new person on the server'''
	async with httpx.AsyncClient() as client:
		response = await client.post(BASE_URL, json={"name": name, "number": number})
	response.raise_for_status()
	return Person(**response.json())

async def delete_person(person_id: str) -> None:
	'''Delete a person on the server'''
	async with httpx.AsyncClient() as client:
		response = await client.delete(f"{BASE_URL}/{person_id}")
	response.raise_for_status()

async def update_number(person_id: str, number: str) -> Person:
	async with httpx.AsyncClient() as client:
		response = await client.patch(f"{BASE_URL}/{person_id}", json={"number": number})
	response.raise_for_status()
	return Person(**response.json())