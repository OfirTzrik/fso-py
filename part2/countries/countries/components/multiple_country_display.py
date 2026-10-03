import reflex as rx

from .single_country_display import single_country_display

from ..models import Country

def multiple_country_display(computed_var: rx.vars.ArrayVar[list[Country]]) -> rx.Component:
	return rx.el.div(
		rx.cond(
			computed_var.length() > 10,
			rx.el.p("Too many matches, specify another filter"),
			rx.cond(
				(computed_var.length() >= 2) & (computed_var.length() <= 10),
				rx.foreach(
					computed_var,
					lambda country: rx.el.div(
						rx.el.p(country.name),
						key=country.name,
					),
				),
				rx.cond(
					computed_var.length() == 1,
					single_country_display(computed_var[0])
				),
			),
		),
	)