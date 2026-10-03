import reflex as rx

from ..models import Weather

def weather_display(weather: rx.vars.ObjectVar[Weather]) -> rx.Component:
	return rx.el.div(
		rx.el.p(f"Temperature: {weather.temp} degrees celsius"),
		rx.el.p(f"Wind speed: {weather.wind} km/h"),
		rx.el.img(src=f"https://openweathermap.org/img/wn/{weather.icon}@2x.png"),
		class_name="weather"
	)