"""This file is used to describe the different bodies a request
can have using Pydantic models, any bodies that don't follow the
rules specified here are denied with 422 Unprocessable Content"""

from pydantic import BaseModel, ConfigDict, Field, field_validator


# For POST
# Does not contain 'id' because it is created server-side
class NoteCreate(BaseModel):
	# ConfigDict is a set of "switches" we want to be active
	# for the entire model and not just a single one ('Field'
	# does that for a single field in the model).
	# Pydantic looks for 'model_config' so that name is fixed.
	model_config = ConfigDict(str_strip_whitespace=True)

	# 'Field' attaches rules to a field
	content: str = Field(min_length=5, max_length=200)
	important: bool = False

	# Custom rule that can't be expressed as 'Field'
	# This one specifically tells Pydantic to run this custom
	# rule on the 'content' field.
	@field_validator("content")
	# @classmethod is required by Pydantic; unused.
	@classmethod
	# 'value' arrives to the method after the rules above have
	# already been applied so it is stripped of whitespaces and
	# has the expected length.
	def not_shouting(cls, value: str) -> str:
		if value.isupper():
			raise ValueError("content must not be written in all capital letters")
		return value


# For PATCH
# Needs to follow the same rules as NoteCreate
class NoteUpdate(BaseModel):
	model_config = ConfigDict(str_strip_whitespace=True)

	# | None mean the field can be null and default=None makes
	# the field optional.
	content: str | None = Field(default=None, min_length=1, max_length=200)
	important: bool | None = None

	@field_validator("content")
	@classmethod
	def not_shouting(cls, value: str | None) -> str:
		if value is None:
			return value
		if value.isupper():
			raise ValueError("content must not be written in all capital letters")
		return value


# What responses contain
class NoteOut(BaseModel):
	# from_attributes tells Pydantic to read the data like
	# Python reads objects (data.field_name) and not how it
	# reads by default (which is reading dicts like
	# data["field_name"])
	model_config = ConfigDict(from_attributes=True)

	id: int
	content: str
	important: bool
