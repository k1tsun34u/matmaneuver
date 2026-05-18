from dataclasses import dataclass
from datetime import datetime
from app.models.public.base_model import BaseModel

@dataclass
class Warehouse(BaseModel):
	id: int
	address: str
	description: str | None
	deleted_by: int | None
	deleted_at: datetime | None
	created_by: int | None
	created_at: datetime