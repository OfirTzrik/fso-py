import re

from pydantic import BaseModel, ConfigDict, Field, field_validator


class PersonCreate(BaseModel):
	model_config = ConfigDict(str_strip_whitespace=True)

	name: str = Field(min_length=3)
	number: str = Field(min_length=8)

	@field_validator("number")
	@classmethod
	def number_pattern(cls, value: str) -> str:
		if not bool(re.fullmatch(r"[0-9]{2,3}-[0-9]+", value)):
			raise ValueError("number must look like 09-1234567: 2-3 digits, a dash, then digits")
		return value


class PersonUpdate(BaseModel):
	model_config = ConfigDict(str_strip_whitespace=True)

	number: str = Field(min_length=8)

	@field_validator("number")
	@classmethod
	def number_pattern(cls, value: str) -> str:
		if not bool(re.fullmatch(r"[0-9]{2,3}-[0-9]+", value)):
			raise ValueError("number must look like 09-1234567: 2-3 digits, a dash, then digits")
		return value


class PersonOut(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	id: int
	name: str
	number: str
