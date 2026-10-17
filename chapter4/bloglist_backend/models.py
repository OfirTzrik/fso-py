from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Blog(Base):
	__tablename__ = "blogs"

	id: Mapped[int] = mapped_column(primary_key=True)
	title: Mapped[str]
	author: Mapped[str]
	url: Mapped[str]
	likes: Mapped[int] = mapped_column(default=0)
