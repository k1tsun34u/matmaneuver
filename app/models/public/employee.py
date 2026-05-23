from dataclasses import dataclass
from datetime import date, datetime
from app.models.public.base_model import BaseModel

@dataclass
class Employee(BaseModel):
	id: int
	user_id: int
	hired_by: int | None
	hired_at: date
	fired_by: int | None
	fired_at: date | None
	created_by: int | None
	created_at: datetime
	
	COLUMN_ID = "id"
	COLUMN_USER_ID = "user_id"
	COLUMN_HIRED_BY = "hired_by"
	COLUMN_HIRED_AT = "hired_at"
	COLUMN_FIRED_BY = "fired_by"
	COLUMN_CREATED_BY = "created_by"
