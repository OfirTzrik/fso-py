'''This file is used to describe the different bodies a request
can have using Pydantic models'''

from pydantic import BaseModel, ConfigDict, Field, field_validator

# For POST
# Does not contain 'id' because it is created server-side
class NoteCreate(BaseModel):
	model_config = ConfigDict(str_strip_whitespace=True)
	# 'Field' attaches rules to a field
	content: str = Field(min_length=5, max_length=200)
	important: bool = False

	# 'value' the the field's (content) value, which arrives
	# after the rules above which means it arrives with the
	# proper length and stripped for whitespaces.
	@field_validator("content")
	@classmethod
	def not_shouting(cls, value: str) -> str:
		if value.isupper():
			raise ValueError("content must not be written in all capital letter")
		return value

# For PATCH
# Needs to follow the same rules as NoteCreate
class NoteUpdate(BaseModel):
	content: str | None = Field(default=None, min_length=1, max_length=200)
	important: bool | None = None

# What responses contain
class NoteOut(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	id: int
	content: str
	important: bool