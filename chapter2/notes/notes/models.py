from dataclasses import dataclass

@dataclass
class Note:
	id: str
	content: str
	important: bool