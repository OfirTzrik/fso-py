import reflex as rx

def notification(message: rx.Var[str]) -> rx.Component:
	return rx.cond(
		message,
		rx.el.div(
			message,
			class_name="error",
		),
	)