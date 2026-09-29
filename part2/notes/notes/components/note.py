import reflex as rx
from ..models import Note

def note(data: rx.vars.ObjectVar[Note]) -> rx.Component:
	return rx.el.li(data.content)