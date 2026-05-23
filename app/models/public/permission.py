from datetime import datetime
from dataclasses import dataclass
from app.models.public.base_model import BaseModel

@dataclass
class Permission(BaseModel):
	id: int
	code: str
	description: str | None
	is_system: bool
	deactivated_by: int | None
	deactivated_at: datetime | None
	created_by: int | None
	created_at: datetime

	COLUMN_ID = "id"
	COLUMN_CODE = "code"
	COLUMN_DESCRIPTION = "description"
	COLUMN_IS_SYSTEM = "is_system"
	COLUMN_DEACTIVATED_BY = "deactivated_by"
	COLUMN_CREATED_BY = "created_by"

	HIRE_EMPLOYEE = "hire"
	FIRE_EMPLOYEE = "fire"
	CREATE_EMPLOYEE = "create_employee"