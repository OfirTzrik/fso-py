import reflex as rx

def search_filter(filter_var: rx.vars.StringVar[str], filter_handler) -> rx.Component:
	return rx.el.div(
		"filter shown with",
		rx.el.input(
			value=filter_var,
			on_change=filter_handler,
			placeholder="Filter by name",
		),
	)