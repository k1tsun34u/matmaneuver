from dataclasses import dataclass
from datetime import datetime
from app.models.public.base_model import BaseModel

@dataclass
class Category(BaseModel):
	id: int
	parent_category_id: int | None
	name: str
	deactivated_by: int | None
	deactivated_at: datetime | None
	created_by: int | None
	created_at: datetime
