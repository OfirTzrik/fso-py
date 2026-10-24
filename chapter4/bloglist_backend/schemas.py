from pydantic import BaseModel, ConfigDict


class BlogCreate(BaseModel):
	title: str
	author: str
	url: str
	likes: int = 0


class BlogOut(BaseModel):
	model_config = ConfigDict(from_attributes=True)
	id: int
	title: str
	author: str
	url: str
	likes: int


class BlogUpdate(BaseModel):
	likes: int
