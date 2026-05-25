from typing import ClassVar
from datetime import datetime
from dataclasses import dataclass
from app.models.public.base_model import BaseModel

@dataclass
class EmployeeRole(BaseModel):
	COLUMN_EMPLOYEE_ID: ClassVar[str] = "employee_id"
	COLUMN_ROLE_ID: ClassVar[str] = "role_id"
	COLUMN_ASSIGNED_BY: ClassVar[str] = "assigned_by"
	COLUMN_ASSIGNED_AT: ClassVar[str] = "assigned_at"
	
	TABLE: ClassVar[str] = "employee_roles"
	ENTITY: ClassVar[str] = "EmployeeRole"

	employee_id: int
	role_id: int
	assigned_by: int | None
	assigned_at: datetime
