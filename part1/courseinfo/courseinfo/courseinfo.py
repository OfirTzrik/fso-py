import reflex as rx
from typing import TypedDict

# Part is a dictionary where name is str and exercises is int
# Removes the vagueness of types
class Part(TypedDict):
	name: str
	exercises: int

# Course similar reasoning to Part
class Course(TypedDict):
	name: str
	parts: list[Part]

def header(course_name: str) -> rx.Component:
	return rx.el.h1(f"{course_name}")

def part(p: Part) -> rx.Component:
	return rx.el.p(f"{p["name"]} {p["exercises"]}")

def content(parts: list[Part]) -> rx.Component:
	return rx.fragment(
		*[part(p) for p in parts],
	)

def total(parts: list[Part]) -> rx.Component:
	exercises_list = [d["exercises"] for d in parts]
	return rx.el.p(f"Number of exercises {sum(exercises_list)}")

def index() -> rx.Component:
	course: Course = {
		"name": "Half stack application development",
		"parts": [
			{
				"name": "Fundamentals of Reflex",
				"exercises": 10,
			},
			{
				"name": "Using arguments to pass data",
				"exercises": 7,
			},
			{
				"name": "State of a component",
				"exercises": 14,
			},
		]
	}
	

	return rx.fragment(
		header(course["name"]),
		content(course["parts"]),
		total(course["parts"]),
	)

app = rx.App()
app.add_page(index)