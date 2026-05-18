from dataclasses import dataclass
from datetime import datetime
from app.models.public.base_model import BaseModel

@dataclass
class PublicUser(BaseModel):
	id: int
	phone: str
	email: str | None
	full_name: str
	blocked_at: datetime | None
	deleted_at: datetime | None
	created_at: datetime