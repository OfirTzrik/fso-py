import reflex as rx

def header(course_name: str) -> rx.Component:
	return rx.el.h1(f"{course_name}")

def part(part_name: str, num_exercises: int) -> rx.Component:
	return rx.el.p(f"{part_name} {num_exercises}")

def content(parts_and_exercises: list[tuple[str, int]]) -> rx.Component:
	p_e1, p_e2, p_e3 = parts_and_exercises

	return rx.fragment(
		part(p_e1[0], p_e1[1]),
		part(p_e2[0], p_e2[1]),
		part(p_e3[0], p_e3[1]),
	)

def total(exercises: list[int]) -> rx.Component:
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
		content([(part1, exercises1), (part2, exercises2), (part3, exercises3)]),
		total([exercises1, exercises2, exercises3])
	)

app = rx.App()
app.add_page(index)