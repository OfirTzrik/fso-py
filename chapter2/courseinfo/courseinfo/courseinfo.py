import reflex as rx
from .components.course import Course, course_view

def index() -> rx.Component:
	courses: list[Course] = [
        {
            "name": "Half Stack application development",
            "id": 1,
            "parts": [
                {"name": "Fundamentals of Reflex", "exercises": 10, "id": 1},
                {"name": "Using arguments to pass data", "exercises": 7, "id": 2},
                {"name": "State of a component", "exercises": 14, "id": 3},
                {"name": "State management", "exercises": 11, "id": 4},
            ],
        },
        {
            "name": "FastAPI",
            "id": 2,
            "parts": [
                {"name": "Routing", "exercises": 3, "id": 1},
                {"name": "Middleware", "exercises": 7, "id": 2},
            ],
        },
    ]
	

	return rx.fragment(
		rx.el.h1("Web development curriculum"),
		rx.el.br(),
		*[course_view(course) for course in courses],
	)

app = rx.App()
app.add_page(index)