import reflex as rx
from .book_registry import book_registry
from ..models import Person

def book_list(names_after_filter: rx.vars.ArrayVar[list[Person]], ask_delete) -> rx.Component:
	return rx.el.div(
		rx.el.h2("Numbers"),
		rx.el.ul(
			rx.foreach(names_after_filter, lambda p: book_registry(p, ask_delete)),
		),
	)