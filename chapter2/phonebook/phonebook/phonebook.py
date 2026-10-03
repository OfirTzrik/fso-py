import reflex as rx
from .state import PhonebookState
from .components.search_filter import search_filter
from .components.form import form
from .components.book_list import book_list
from .components.notification import success_message

def index() -> rx.Component:
	return rx.el.div(
		rx.el.h2("Phonebook", class_name="title"),
		success_message(PhonebookState.notification_text, PhonebookState.curr_class),
		search_filter(PhonebookState.filter_name, PhonebookState.on_change_filter),
		form(
			PhonebookState.new_name,
			PhonebookState.on_change_name,
			PhonebookState.new_number,
			PhonebookState.on_change_number,
			PhonebookState.on_submit,
		),
		book_list(PhonebookState.persons_to_show, PhonebookState.ask_delete),
	)

app = rx.App(stylesheets=["styles.css"])
app.add_page(index, on_load=PhonebookState.load_people)