from dataclasses import dataclass

@dataclass
class Note:
	id: int
	content: str
	important: bool