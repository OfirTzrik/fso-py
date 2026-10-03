import reflex as rx

def footer() -> rx.Component:
	return rx.el.div(
		rx.el.br(),
		rx.el.em("Note app, Department of Computer Science"),
		color="green",
		font_style="italic",
		font_size="16px",
	)