import reflex as rx
from collections.abc import Sequence

class ClickState(rx.State):
	left: rx.Field[int] = rx.field(0)
	right: rx.Field[int] = rx.field(0)
	all_clicks: rx.Field[list[str]] = rx.field([])

	@rx.event
	def click_left(self):
		self.all_clicks.append("L")
		self.left += 1

	@rx.event
	def click_right(self):
		self.all_clicks.append("R")
		self.right += 1

	@rx.var
	def total(self) -> int:
		return self.left + self.right

# Reflex describes list Vars with the wider type (Sequence) and not with 'list'
# PyLance expects rx.vars.ArrayVar[Sequence[str]] and not rx.vars.ArrayVar[list[str]]
def history(all_clicks: rx.vars.ArrayVar[Sequence[str]]) -> rx.Component:
	return rx.cond(
		all_clicks.length() == 0,
		rx.el.div("the app is used by pressing the buttons"),
		rx.el.div("button press history: ", all_clicks.join(" ")),
	)

def button(on_click, text: str) -> rx.Component:
	return rx.el.button(text, on_click=on_click)

def index() -> rx.Component:
	return rx.el.div(
		ClickState.left,
		button(ClickState.click_left, "left"),
		button(ClickState.click_right, "right"),
		rx.el.button("right", on_click=ClickState.click_right),
		ClickState.right,
		history(ClickState.all_clicks),
		rx.el.p(f"total is {ClickState.total}")
	)

app = rx.App()
app.add_page(index)