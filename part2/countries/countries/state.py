import reflex as rx

from .models import Country
from .services.country_service import get_all_countries

class CountryState(rx.State):
	name_filter: rx.Field[str] = rx.field("")
	_all_countries: rx.Field[list[Country]] = rx.field(default_factory=list)

	@rx.event
	async def on_load(self):
		'''When the page loads, get all 250 countries'''
		self._all_countries = await get_all_countries()

	@rx.event
	def on_change_filter(self, value: str):
		'''Function to run whenever the filter-input's value is changing'''
		self.name_filter = value

	@rx.var
	def list_filter(self) -> list[Country]:
		'''Computed var for displaying only countries that match the filter,
		meaning display countries that there's a match with their name'''
		return [country for country in self._all_countries if self.name_filter.lower() in country.name.lower()]