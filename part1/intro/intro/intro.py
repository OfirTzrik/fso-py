from datetime import datetime
import reflex as rx

def hello(name: str, age: int) -> rx.Component:
	return rx.fragment(
		rx.el.p(f"Hello {name}, you are {age} years old"),
	)

def index() -> rx.Component:
	name = "Ofir"
	age = 28

	return rx.fragment(
		rx.el.h1("Greetings"),
		hello("Maya", 24),
		hello(name=name, age=age),
	)

app = rx.App()
app.add_page(index)