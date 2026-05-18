from dataclasses import dataclass
from datetime import datetime
from app.models.public.base_model import BaseModel

@dataclass
class EmployeeRole(BaseModel):
	employee_id: int
	role_id: int
	assigned_by: int | None
	assigned_at: datetime