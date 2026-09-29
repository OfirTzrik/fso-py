from typing import TypedDict
import reflex as rx

class Note(TypedDict):
	id: int
	content: str
	important: bool

def note(data: Note) -> rx.Component:
	return rx.el.li(data["content"])