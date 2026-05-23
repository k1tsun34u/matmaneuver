from dataclasses import dataclass
from datetime import datetime
from app.models.public.base_model import BaseModel

@dataclass
class Role(BaseModel):
	id: int
	code: str
	is_system: bool
	deactivated_by: int | None
	deactivated_at: datetime | None
	created_by: int | None
	created_at: datetime

	COLUMN_ID = "id"
	COLUMN_CODE = "code"
	COLUMN_IS_SYSTEM = "is_system"
	COLUMN_DEACTIVATED_BY = "deactivated_by"
	COLUMN_CREATED_BY = "created_by"
