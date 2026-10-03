import reflex as rx

from ..models import Country

def single_country_display(country: rx.vars.ObjectVar[Country]) -> rx.Component:
	'''Display a single country's details since the filter is now specific
	enough to show a single country's details'''
	return rx.el.div(
		rx.el.p(f"Name: {country.name}"),
		rx.el.p(
			rx.cond(
				country.capital,
				f"Capital city: {country.capital}",
				"",
			),
		),
		rx.el.p(f"Area in square kilometers: {country.area}"),
		rx.cond(
			country.languages,
			rx.fragment(
				rx.el.p("Official languages:"),
				rx.el.ul(rx.foreach(country.languages, rx.el.li)),
			),
		),

		rx.el.img(src=country.flag),
	)