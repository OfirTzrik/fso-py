from pydantic import BaseModel, ConfigDict, Field

# For POST
# Does not contain 'id' because it is created server-side
class NoteCreate(BaseModel):
	content: str = Field(min_length=1)
	important: bool = False

# For PATCH
class NoteUpdate(BaseModel):
	content: str | None = Field(default=None, min_length=1)
	important: bool | None = None

# What responses contain
class NoteOut(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	id: int
	content: str
	important: bool