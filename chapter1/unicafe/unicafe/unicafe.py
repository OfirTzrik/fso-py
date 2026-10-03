import reflex as rx
from decimal import Decimal

class FeedbackState(rx.State):
	good: rx.Field[int] = rx.field(0)
	neutral: rx.Field[int] = rx.field(0)
	bad: rx.Field[int] = rx.field(0)

	@rx.event
	def give_good(self):
		self.good += 1

	@rx.event
	def give_neutral(self):
		self.neutral += 1

	@rx.event
	def give_bad(self):
		self.bad += 1

	@rx.var
	def total(self) -> int:
		return self.good + self.neutral + self.bad

	@rx.var
	def average(self) -> float:
		total: int = self.good + self.neutral + self.bad
		if total == 0:
			return 0.0
		return (self.good - self.bad) / total

	@rx.var
	def positive(self) -> float:
		total: int = self.good + self.neutral + self.bad
		if total == 0:
			return 0.0
		return (self.good / (self.good + self.neutral + self.bad)) * 100.0

def heading(text: str) -> rx.Component:
	return rx.el.h1(f"{text}")

def button(text: str, handler) -> rx.Component:
	return rx.el.button(text, on_click=handler)

def stat(text: str, val: rx.vars.NumberVar[int | float | Decimal], is_percent: bool) -> rx.Component:
	if not is_percent:
		return rx.el.tr(
			rx.el.td(text),
			rx.el.td(val),
		)
	return rx.el.tr(
		rx.el.td(text),
		rx.el.td(f"{val} %"),
	)

def statistics() -> rx.Component:
	return rx.el.table(
		rx.el.tbody(
			stat("good", FeedbackState.good, False),
			stat("neutral", FeedbackState.neutral, False),
			stat("bad", FeedbackState.bad, False),
			stat("all", FeedbackState.total, False),
			stat("average", FeedbackState.average, False),
			stat("positive", FeedbackState.positive, True),
		)
	)

def index() -> rx.Component:
	# Regular int when in the class, NumberVar outside
	total: rx.vars.NumberVar[int | float | Decimal] = FeedbackState.good + FeedbackState.neutral + FeedbackState.bad

	return rx.cond(
		total == 0,
		rx.fragment(
			heading("give feedback"),
			button("good", FeedbackState.give_good),
			button("neutral", FeedbackState.give_neutral),
			button("bad", FeedbackState.give_bad),
			heading("statistics"),
			rx.el.p(f"no feedback given"),
		),
		rx.fragment(
			heading("give feedback"),
			button("good", FeedbackState.give_good),
			button("neutral", FeedbackState.give_neutral),
			button("bad", FeedbackState.give_bad),
			heading("statistics"),
			statistics(),
		),
	)

app = rx.App()
app.add_page(index)