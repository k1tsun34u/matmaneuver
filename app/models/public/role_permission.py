from dataclasses import dataclass
from datetime import datetime
from app.models.public.base_model import BaseModel

@dataclass
class RolePermission(BaseModel):
	role_id: int
	permission_id: int
	assigned_by: int | None
	assigned_at: datetime