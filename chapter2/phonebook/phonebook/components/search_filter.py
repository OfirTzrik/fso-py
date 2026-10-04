import reflex as rx

def search_filter(filter_var: rx.vars.StringVar[str], filter_handler) -> rx.Component:
	return rx.el.div(
		"filter shown with: ",
		rx.debounce_input(
			rx.el.input(
				value=filter_var,
				on_change=filter_handler,
				placeholder="Filter by name",
			),
			force_notify_by_enter=True,
			force_notify_on_blur=True,
		),
	)