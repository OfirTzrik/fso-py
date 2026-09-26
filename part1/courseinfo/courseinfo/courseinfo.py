import reflex as rx

def header(course_name: str) -> rx.Component:
	return rx.el.h1(f"{course_name}")

def part(part_name: str, num_exercises: int) -> rx.Component:
	return rx.el.p(f"{part_name} {num_exercises}")

def content(parts_and_exercises: list[tuple[str, int]]) -> rx.Component:
	return rx.fragment(
		*[part(p, e) for p, e in parts_and_exercises],
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