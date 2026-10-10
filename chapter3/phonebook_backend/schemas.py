from pydantic import BaseModel, ConfigDict, Field

class PersonCreate(BaseModel):
	name: str = Field(min_length=1)
	number: str = Field(min_length=1)

class PersonUpdate(BaseModel):
	number: str = Field(min_length=1)

class PersonOut(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	id: int
	name: str
	number: str