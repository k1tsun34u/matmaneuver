from dataclasses import dataclass
from datetime import datetime
from app.models.public.base_model import BaseModel

@dataclass
class Supplier(BaseModel):
	id: int
	name: str
	phone: str
	email: str | None
	address: str | None
	deactivated_by: int | None
	deactivated_at: datetime | None
	created_by: int | None
	created_at: datetime
