import reflex as rx

def country_filter(country_name: rx.Var[str], country_filter_handler) -> rx.Component:
	return rx.el.div(
		"Filter countries: ",
		rx.el.input(
			# Update the input field along with the state var
			value=country_name,
			on_change=country_filter_handler,
			placeholder="Country name here...",
		),
	)