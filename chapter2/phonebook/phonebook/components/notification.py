import reflex as rx

def success_message(message: rx.Var[str], curr_class: rx.Var[str]) -> rx.Component:
	return rx.cond(
		message,
		rx.el.div(
			message,
			class_name=curr_class,
		),
	)