from dataclasses import dataclass

@dataclass
class Country:
	name: str
	capital: str
	area: float
	languages: list[str]
	flag: str

@dataclass
class Weather:
	temp: float	
	wind: float
	icon: str