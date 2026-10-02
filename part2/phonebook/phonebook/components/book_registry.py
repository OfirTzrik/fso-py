import reflex as rx
from ..models import Person

# Show the names of the persons on the list of Person(s) to be displayed
def book_registry(person: rx.vars.ObjectVar[Person], ask_delete) -> rx.Component:
	return rx.el.li(
		f"{person.name} {person.number}",
		" ",
		rx.el.button("DELETE", on_click=lambda: ask_delete(person.id)),
		key=person.id,
	)