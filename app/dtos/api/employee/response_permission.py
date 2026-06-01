from datetime import datetime
from dataclasses import dataclass
from app.models.public.permission import Permission

@dataclass
class ResponsePermission:
	id: int
	code: str
	description: str | None
	is_system: bool
	deactivated_by: int | None
	deactivated_at: datetime | None
	created_by: int | None
	created_at: datetime

	def __init__(self, permission: Permission):
		self.id = permission.id
		self.code = permission.code
		self.description = permission.description
		self.is_system = permission.is_system
		self.deactivated_by = permission.deactivated_by
		self.deactivated_at = permission.deactivated_at
		self.created_by = permission.created_by
		self.created_at = permission.created_at
