from datetime import datetime
from dataclasses import dataclass
from app.models.public.employee import Employee

@dataclass
class ResponseEmployee:
	id: int
	user_id: int
	hired_by: int | None
	hired_at: datetime | None
	fired_by: int | None
	fired_at: datetime | None
	created_by: int | None
	created_at: datetime

	def __init__(self, employee: Employee):
		self.id = employee.id
		self.user_id = employee.user_id
		self.hired_by = employee.hired_by
		self.hired_at = employee.hired_at
		self.fired_by = employee.fired_by
		self.fired_at = employee.fired_at
		self.created_by = employee.created_by
		self.created_at = employee.created_at
