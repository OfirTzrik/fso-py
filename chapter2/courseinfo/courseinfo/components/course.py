import reflex as rx
from typing import TypedDict
from functools import reduce

# Part is a dictionary where name is str and exercises is int
# Removes the vagueness of types
class Part(TypedDict):
	id: int
	name: str
	exercises: int

# Course similar reasoning to Part
class Course(TypedDict):
	id: int
	name: str
	parts: list[Part]

def header(course_name: str) -> rx.Component:
	return rx.el.h2(f"{course_name}")

def part(p: Part) -> rx.Component:
	return rx.el.p(f"{p["name"]} {p["exercises"]}")

def content(parts: list[Part]) -> rx.Component:
	return rx.fragment(
		*[part(p) for p in parts],
	)

def total(parts: list[Part]) -> rx.Component:
	exercises_list = [d["exercises"] for d in parts]
	return rx.el.p(f"Number of exercises {sum(exercises_list)}")

# 'total' written using 'reduce' instead of using 'sum'
def total_reduce(parts: list[Part]) -> rx.Component:
	r = reduce(lambda cumm, curr: cumm + curr["exercises"], parts, 0)
	return rx.el.p(
		rx.el.strong(f"total of exercises {r}"),
	)

def course_view(course_info: Course) -> rx.Component:
	return rx.fragment(
		header(course_info["name"]),
		content(course_info["parts"]),
		total_reduce(course_info["parts"]),
	)