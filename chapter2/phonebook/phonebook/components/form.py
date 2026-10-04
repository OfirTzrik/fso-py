import reflex as rx

def form(name_var: rx.vars.StringVar[str], name_change_handler, number_var: rx.vars.StringVar[str], number_change_handler, submit_handler) -> rx.Component:
	return rx.el.form(
		rx.el.div(
			"name: ",
			rx.debounce_input(
				rx.el.input(
					value=name_var,
					on_change=name_change_handler,
					placeholder="New name here",
				),
				force_notify_by_enter=True,
				force_notify_on_blur=True,
			),
		),
		rx.el.div(
			"number: ",
			rx.debounce_input(
				rx.el.input(
					value=number_var,
					on_change=number_change_handler,
					placeholder="New number here",
				),
				force_notify_by_enter=True,
				force_notify_on_blur=True,
			),
		),
		rx.el.div(
			rx.el.button("add", type="submit"),
		),
		on_submit=submit_handler,
	)