import reflex as rx

from .models import Country
from .models import Weather
from .services.country_service import get_all_countries
from .services.weather_service import get_weather_capital

class CountryState(rx.State):
	name_filter: rx.Field[str] = rx.field("")
	_all_countries: rx.Field[list[Country]] = rx.field(default_factory=list)
	selected: rx.Field[Country | None] = rx.field(None)
	weather: rx.Field[Weather | None] = rx.field(None)

	@rx.event
	async def on_load(self):
		'''When the page loads, get all 250 countries'''
		self._all_countries = await get_all_countries()

	@rx.event
	def on_change_filter(self, value: str):
		'''Function to run whenever the filter-input's value is changing'''
		self.name_filter = value
		if len(self.list_filter) == 1:
			self.selected = self.list_filter[0]
			return CountryState.capital_weather()
		else:
			self.selected = None
			self.weather = None

	@rx.event
	def show_country(self, country_name: str):
		self.selected = next(c for c in self._all_countries if c.name == country_name)
		return CountryState.capital_weather()

	@rx.event
	async def capital_weather(self):
		if self.selected is None or not self.selected.capital:
			return
		self.weather = await get_weather_capital(self.selected.capital)

	@rx.var
	def list_filter(self) -> list[Country]:
		'''Computed var for displaying only countries that match the filter,
		meaning display countries that there's a match with their name'''
		return [country for country in self._all_countries if self.name_filter.lower() in country.name.lower()]