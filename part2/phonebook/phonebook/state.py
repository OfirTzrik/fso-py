import typing
import reflex as rx
import json
import asyncio
import httpx
from .models import Person
from .services import person_service

class PhonebookState(rx.State):
	persons: rx.Field[list[Person]] = rx.field(default_factory=list)
	new_name: rx.Field[str] = rx.field("")
	new_number: rx.Field[str] = rx.field("")
	filter_name: rx.Field[str] = rx.field("")
	notification_text: rx.Field[str] = rx.field("")
	curr_class: rx.Field[str] = rx.field("success")

	@rx.event
	async def update_person_number(self, person_id: str, number: str, confirmed: bool):
		if not confirmed:
			return
		try:
			updated = await person_service.update_number(person_id, number)
		except httpx.HTTPStatusError as error:
			person = next(p for p in self.persons if p.id == person_id)
			if error.response.status_code == 404:
				self.persons = [p for p in self.persons if p.id != person_id]
				self.curr_class = "failure"
				self.notification_text = f"Person '{person.name}' was already removed from the server"
				return PhonebookState.clear_notification_after
			raise
		self.persons = [updated if p.id == person_id else p for p in self.persons]
		self.curr_class = "success"
		self.notification_text = f"Existing person '{updated.name}' was successfully updated"
		self.new_name = ""
		self.new_number = ""
		return PhonebookState.clear_notification_after

	# When submitting the form
	@rx.event
	async def on_submit(self, form_data: dict[str, typing.Any]):
		'''Make the necessary checks before adding a new person to the list'''
		# Check missing information
		if not self.new_name or not self.new_number:
			return rx.window_alert(f"Missing name and / or number")

		# Check duplicate by name
		existing = next((p for p in self.persons if p.name.lower() == self.new_name.lower()), None)
		if existing is not None:
			message = f"{existing.name} is already added to phonebook, replace the old number with a new one?"
			return rx.call_script(
				f"window.confirm({json.dumps(message)})",
				callback=lambda result: PhonebookState.update_person_number(existing.id, self.new_number, result),
			)

		# Make the change (update on server and then locally)
		response = await person_service.create_person(self.new_name, self.new_number)
		self.persons.append(response)
		self.curr_class = "success"
		self.notification_text = f"New person '{self.new_name}' was successfully added"
		self.new_name = ""
		self.new_number = ""
		return PhonebookState.clear_notification_after

	@rx.event(background=True)
	async def clear_notification_after(self):
		await asyncio.sleep(5)
		async with self:
			self.notification_text = ""

	@rx.event
	def on_change_name(self, value: str):
		self.new_name = value

	@rx.event
	def on_change_number(self, value: str):
		self.new_number = value

	@rx.event
	def on_change_filter(self, value: str):
		self.filter_name = value

	@rx.event
	async def load_people(self):
		'''Get the list of persons from the server and update the local list'''
		self.persons = await person_service.get_persons()

	@rx.event
	async def delete_person(self, person_id: str, confirmed: bool):
		'''Runs after the confirm dialog closes; deletes on the server, then locally'''
		if not confirmed:
			return
		try:
			response = await person_service.delete_person(person_id)
		except httpx.HTTPStatusError as error:
			person = next(p for p in self.persons if p.id == person_id)
			if error.response.status_code == 404:
				self.persons = [p for p in self.persons if p.id != person_id]
				self.curr_class = "failure"
				self.notification_text = f"Person '{person.name}' was already removed from the server"
				return PhonebookState.clear_notification_after
		self.persons = [p for p in self.persons if p.id != person_id]

	@rx.event
	def ask_delete(self, person_id: str):
		'''Ask the user to confirm before deleting'''
		person = next(p for p in self.persons if p.id == person_id)
		message = f"Delete {person.name}?"
		return rx.call_script(
			f"window.confirm({json.dumps(message)})",
			callback=lambda result: PhonebookState.delete_person(person_id, result),
		)

	@rx.var
	def persons_to_show(self) -> list[Person]:
		'''Choose which persons to show based on name filtering'''
		filtered = list(filter(lambda person: self.filter_name.lower() in person.name.lower(), self.persons))
		return filtered