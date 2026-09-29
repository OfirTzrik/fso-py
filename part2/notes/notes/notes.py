import reflex as rx
from .components.note import Note, note

NOTES: list[Note] = [
	{
		"id": 1,
		"content": "HTML is easy",
		"important": True,
	},
	{
		"id": 2,
		"content": "Browser can only execute only JavaScript",
		"important": False,
	},
	{
		"id": 3,
		"content": "GET and POST are the most important methods of HTTP protocol",
		"important": True,
	},
]

def index() -> rx.Component:
	return rx.fragment(
		rx.el.h1("Notes"),
		rx.el.ul(
			*[note(n) for n in NOTES],
		),
	)

app = rx.App()
app.add_page(index)