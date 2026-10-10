'''Add new entries and view existing entries using the cli
usage: python3 cli.py "<name>" <number>'''

import sys
from sqlalchemy import select

from database import Base, SessionLocal, engine
from models import Person

Base.metadata.create_all(engine)

with SessionLocal() as db:
	# Retrieve existing entries
	if len(sys.argv) == 1:
		persons = db.scalars(select(Person)).all()
		print("phonebook:")
		for person in persons:
			print(f"{person.name} {person.number}")
	# Add new entry
	elif len(sys.argv) == 3:
		name = sys.argv[1]
		number = sys.argv[2]
		person = Person(name=name, number=number)
		db.add(person)
		db.commit()
		db.refresh(person)
		print(f"added {name} number {number} to phonebook")
	# Bad number of command line arguments
	else:
		print("usage: python3 cli.py \"<name>\" <number>")