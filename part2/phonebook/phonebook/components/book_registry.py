import reflex as rx
from ..models import Person

# Show the names of the persons on the list of Person(s) to be displayed
def book_registry(person: rx.vars.ObjectVar[Person]) -> rx.Component:
	return rx.el.li(
		f"{person.name} {person.number}"
	)