import reflex as rx

from .state import CountryState
from .components.country_filter import country_filter
from .components.multiple_country_display import multiple_country_display

def index() -> rx.Component:
    return rx.fragment(
        rx.el.h1("Data for countries"),
        country_filter(CountryState.name_filter, CountryState.on_change_filter),
        rx.divider(class_name="divider"),
        multiple_country_display(CountryState.list_filter)
	)

app = rx.App(stylesheets=["/styles.css"])
app.add_page(index, on_load=CountryState.on_load)
