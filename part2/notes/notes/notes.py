import reflex as rx
import typing
import httpx
from random import random
from .components.note import note
from .models import Note
from .services import note_service

class NoteState(rx.State):
	notes: rx.Field[list[Note]] = rx.field(default_factory=list)
	new_note: rx.Field[str] = rx.field("a new note...")
	show_all: rx.Field[bool] = rx.field(True)

	# 'form_data' is unused but 'on_submit' still passes it
	@rx.event
	async def add_note(self, form_data: dict[str, typing.Any]):
		created = await note_service.create(content=self.new_note, important=random() < 0.5)
		self.notes.append(created)
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
		self.notes = await note_service.get_all()

	# Toggle the importance of a note provided its id
	@rx.event
	async def toggle_importance(self, note_id: str):
		note = next(n for n in self.notes if n.id == note_id)
		try:
			updated = await note_service.update_important(note_id, not note.important)
		except httpx.HTTPStatusError as error:
			if error.response.status_code == 404:
				self.notes = [n for n in self.notes if n.id != note_id]
				return rx.window_alert(f"the note '{note.content}' was already deleted from the server")
			raise
		self.notes = [updated if n.id == note_id else n for n in self.notes]

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
			rx.foreach(
				NoteState.notes_to_show,
				# Connect the note element and the button on creation
				# (both are created inside the note() function below)
				# to use the toggle_importance function defined in
				# NoteState
				lambda n: note(n, NoteState.toggle_importance),
			),
		),
		rx.el.form(
			rx.el.input(value=NoteState.new_note, on_change=NoteState.set_new_note),
			rx.el.button("save", type="submit"),
			on_submit=NoteState.add_note,
		),
	)

app = rx.App()
app.add_page(index, on_load=NoteState.load_notes)