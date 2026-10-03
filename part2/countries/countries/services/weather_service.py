import httpx
import os

from ..models import Weather

API_KEY = os.environ["WEATHER_API_KEY"]
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

async def get_weather_capital(capital_city: str):
	async with httpx.AsyncClient() as client:
		response = await client.get(WEATHER_URL, params={"q": capital_city, "appid": API_KEY, "units": "metric"})
	data = response.json()
	return Weather(
		temp=data["main"]["temp"],
		wind=data["wind"]["speed"],
		icon=data["weather"][0]["icon"],
	)