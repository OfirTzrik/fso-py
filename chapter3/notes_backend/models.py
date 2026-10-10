from sqlalchemy.orm import Mapped, mapped_column
from database import Base

# All databases inherit from 'Base'
class Note(Base):
	__tablename__ = "notes" # Name of the table in the database

	# Each column in the table
	# All are required unless the type is Mapped[x | None]
	id: Mapped[int] = mapped_column(primary_key=True) # 'id' column will be used as the primary key
	content: Mapped[str]
	important: Mapped[bool] = mapped_column(default=False) # Default value of false