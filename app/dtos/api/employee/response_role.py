from datetime import datetime
from dataclasses import dataclass
from app.models.public.role import Role

@dataclass
class ResponseRole:
	id: int
	code: str
	is_system: bool
	deactivated_by: int | None
	deactivated_at: datetime | None
	created_by: int | None
	created_at: datetime

	def __init__(self, role: Role):
		self.id = role.id
		self.code = role.code
		self.is_system = role.is_system
		self.deactivated_by = role.deactivated_by
		self.deactivated_at = role.deactivated_at
		self.created_by = role.created_by
		self.created_at = role.created_at
