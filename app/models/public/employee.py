from typing import ClassVar
from dataclasses import dataclass
from datetime import datetime
from app.models.public.base_model import BaseModel

@dataclass
class Employee(BaseModel):
	COLUMN_ID: ClassVar[str] = "id"
	COLUMN_USER_ID: ClassVar[str] = "user_id"
	COLUMN_HIRED_BY: ClassVar[str] = "hired_by"
	COLUMN_HIRED_AT: ClassVar[str] = "hired_at"
	COLUMN_FIRED_BY: ClassVar[str] = "fired_by"
	COLUMN_FIRED_AT: ClassVar[str] = "fired_at"
	COLUMN_CREATED_BY: ClassVar[str] = "created_by"
	COLUMN_CREATED_AT: ClassVar[str] = "created_at"

	id: int
	user_id: int
	hired_by: int | None
	hired_at: datetime | None
	fired_by: int | None
	fired_at: datetime | None
	created_by: int | None
	created_at: datetime
