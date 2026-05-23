from typing import ClassVar
from datetime import datetime
from dataclasses import dataclass
from app.models.public.base_model import BaseModel

@dataclass
class RolePermission(BaseModel):
	COLUMN_ROLE_ID: ClassVar[str] = "role_id"
	COLUMN_PERMISSION_ID: ClassVar[str] = "permission_id"
	COLUMN_ASSIGNED_BY: ClassVar[str] = "assigned_by"
	COLUMN_ASSIGNED_AT: ClassVar[str] = "assigned_at"

	role_id: int
	permission_id: int
	assigned_by: int | None
	assigned_at: datetime
