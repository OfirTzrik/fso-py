import reflex as rx
import typing
import httpx
import asyncio
from random import random
from .components.note import note
from .models import Note

BASE_URL = "http://localhost:3001/notes"

class NoteState(rx.State):
	notes: rx.Field[list[Note]] = rx.field(default_factory=list)
	new_note: rx.Field[str] = rx.field("a new note...")
	show_all: rx.Field[bool] = rx.field(True)

	# 'form_data' is unused but 'on_submit' still passes it
	@rx.event
	def add_note(self, form_data: dict[str, typing.Any]):
		self.notes.append(
			Note(
				id=str(len(self.notes) + 1),
				content=self.new_note,
				important=random() < 0.5,
			),
		)
		self.new_note = ""

	# 'on_change' passes the input's current value as a string
	# (here it is passed into the 'value' parameter)
	@rx.event
	def set_new_note(self, value: str):
		self.new_note = value

	@rx.event
	def toggle_show_all(self):
		self.show_all = not self.show_all

	@rx.event
	async def load_notes(self):
		print("load_notes started")
		async with httpx.AsyncClient() as client:
			response = await client.get(BASE_URL)
		print("response received:", response.status_code)
		self.notes = [Note(**n) for n in response.json()]
		print("loaded", len(self.notes), "notes")

	@rx.var
	def notes_to_show(self) -> list[Note]:
		if self.show_all:
			return self.notes
		return [n for n in self.notes if n.important]

def index() -> rx.Component:
	return rx.fragment(
		rx.el.h1("Notes"),
		rx.el.div(
			rx.el.button(
				"show ",
				rx.cond(NoteState.show_all, "important", "all"),
				on_click=NoteState.toggle_show_all,
			),
		),
		rx.el.ul(
			rx.foreach(NoteState.notes_to_show, note),
		),
		rx.el.form(
			rx.el.input(value=NoteState.new_note, on_change=NoteState.set_new_note),
			rx.el.button("save", type="submit"),
			on_submit=NoteState.add_note,
		),
	)

app = rx.App()
app.add_page(index, on_load=NoteState.load_notes)