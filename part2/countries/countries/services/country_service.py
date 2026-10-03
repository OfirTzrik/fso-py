import httpx

from ..models import Country

BASE_URL = "https://studies.cs.helsinki.fi/restcountries/api/all"

async def get_all_countries() -> list[Country]:
	async with httpx.AsyncClient() as client:
		response = await client.get(BASE_URL)
	response.raise_for_status()
	# Not all countries have the 'capital' or 'languages' field, need fallback
	return [Country(
		name=country["name"]["common"],
		capital=(country.get("capital") or [""])[0], # Fallback is list with "nothing"
		area=float(country["area"]),
		languages=list(country.get("languages", {}).values()), # Fallback is empty dictionary
		flag=country["flags"]["png"],
	) for country in response.json()]