from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Person(Base):
	__tablename__ = "persons"

	id: Mapped[int] = mapped_column(primary_key=True)
	name: Mapped[str]
	number: Mapped[str]