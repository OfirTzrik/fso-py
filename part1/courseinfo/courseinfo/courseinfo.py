import reflex as rx

def header(course_name: str) -> rx.Component:
	return rx.fragment(
		rx.el.h1(f"{course_name}"),
	)

def content(parts: list, exercises: list) -> rx.Component:
	part1, part2, part3 = parts
	exercises1, exercises2, exercises3 = exercises

	return rx.fragment(
		rx.el.p(f"{part1} {exercises1}"),
		rx.el.p(f"{part2} {exercises2}"),
		rx.el.p(f"{part3} {exercises3}"),
	)

def total(exercises: list) -> rx.Component:
	return rx.fragment(
		rx.el.p(f"Number of exercises {sum(exercises)}")
	)

def index() -> rx.Component:
	course = "Half stack application development"
	part1 = "Fundamentals of Reflex"
	exercises1 = 10
	part2 = "Using arguments to pass data"
	exercises2 = 7
	part3 = "State of a component"
	exercises3 = 14

	return rx.fragment(
		header(course),
		content([part1, part2, part3], [exercises1, exercises2, exercises3]),
		total([exercises1, exercises2, exercises3])
	)

app = rx.App()
app.add_page(index)