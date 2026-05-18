from dataclasses import dataclass
from datetime import date, datetime
from app.models.public.base_model import BaseModel

@dataclass
class Employee(BaseModel):
	id: int
	user_id: int
	hired_at: date
	fired_by: int | None
	fired_at: date | None
	created_by: int | None
	created_at: datetime