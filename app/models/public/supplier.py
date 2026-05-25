from typing import ClassVar
from datetime import datetime
from dataclasses import dataclass
from app.models.public.base_model import BaseModel

@dataclass
class Supplier(BaseModel):
	COLUMN_ID: ClassVar[str] = "id"
	COLUMN_FULL_NAME: ClassVar[str] = "full_name"
	COLUMN_PHONE: ClassVar[str] = "phone"
	COLUMN_EMAIL: ClassVar[str] = "email"
	COLUMN_ADDRESS: ClassVar[str] = "address"
	COLUMN_DEACTIVATED_BY: ClassVar[str] = "deactivated_by"
	COLUMN_DEACTIVATED_AT: ClassVar[str] = "deactivated_at"
	COLUMN_CREATED_BY: ClassVar[str] = "created_by"
	COLUMN_CREATED_AT: ClassVar[str] = "created_at"

	TABLE: ClassVar[str] = "suppliers"
	ENTITY: ClassVar[str] = "Supplier"

	id: int
	full_name: str
	phone: str
	email: str | None
	address: str | None
	deactivated_by: int | None
	deactivated_at: datetime | None
	created_by: int | None
	created_at: datetime
