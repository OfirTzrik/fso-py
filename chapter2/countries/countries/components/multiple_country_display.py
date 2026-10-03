import reflex as rx

from ..models import Country

def multiple_country_display(computed_var: rx.vars.ArrayVar[list[Country]], show_country_handler) -> rx.Component:
	return rx.el.div(
		rx.cond(
			computed_var.length() > 10,
			rx.el.p("Too many matches, specify another filter"),
			rx.cond(
				(computed_var.length() >= 2) & (computed_var.length() <= 10),
				rx.foreach(
					computed_var,
					lambda country: rx.el.div(
						f"{country.name} ",
						rx.el.button("show", on_click=lambda: show_country_handler(country.name)),
						key=country.name,
					),
				),
			),
		),
	)