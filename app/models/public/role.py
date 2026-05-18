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