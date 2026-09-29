import typing
import reflex as rx
from .models import Person

class PhonebookState(rx.State):
	persons: rx.Field[list[Person]] = rx.field(
		[
			Person(name="Spongebob Squarepants", number="123-456", id=1),
			Person(name="Patrick Star", number="111-222", id=2),
			Person(name="Squidward Tentacles", number="135-791", id=3),
			Person(name="Eugene Krabs", number="246-802", id=4),
		]
	)
	new_name: rx.Field[str] = rx.field("")
	new_number: rx.Field[str] = rx.field("")
	filter_name: rx.Field[str] = rx.field("")

	# When submitting the form
	@rx.event
	def on_submit(self, form_data: dict[str, typing.Any]):
		if not self.new_name or not self.new_number:
			return rx.window_alert(f"Missing name and / or number")
		
		new_person = Person(
			name=self.new_name,
			number=self.new_number,
			id=len(self.persons) + 1,
		)

		if new_person.name in [person.name for person in self.persons]:
			return rx.window_alert(f"{new_person.name} is already added to phonebook")
		
		self.persons.append(new_person)
		self.new_name = ""
		self.new_number = ""

	@rx.event
	def on_change_name(self, value: str):
		self.new_name = value

	@rx.event
	def on_change_number(self, value: str):
		self.new_number = value

	@rx.event
	def on_change_filter(self, value: str):
		self.filter_name = value

	@rx.var
	def persons_to_show(self) -> list[Person]:
		filtered = list(filter(lambda person: self.filter_name.lower() in person.name.lower(), self.persons))
		return filtered