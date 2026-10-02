import reflex as rx
from ..models import Note

def note(data: rx.vars.ObjectVar[Note], toggle_importance) -> rx.Component:
	return rx.el.li(
		data.content,
		" ",
		rx.el.button(
			rx.cond(
				data.important,
				"make not important",
				"make important"
			),
			on_click=lambda: toggle_importance(data.id)
		),
		key=data.id,
	)