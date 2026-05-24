from typing import ClassVar
from datetime import datetime
from dataclasses import dataclass
from app.models.public.base_model import BaseModel

@dataclass
class Warehouse(BaseModel):
	COLUMN_ID: ClassVar[str] = "id"
	COLUMN_ADDRESS: ClassVar[str] = "address"
	COLUMN_DESCRIPTION: ClassVar[str] = "description"
	COLUMN_DELETED_BY: ClassVar[str] = "deleted_by"
	COLUMN_DELETED_AT: ClassVar[str] = "deleted_at"
	COLUMN_CREATED_BY: ClassVar[str] = "created_by"
	COLUMN_CREATED_AT: ClassVar[str] = "created_at"

	ENTITY: ClassVar[str] = "Warehouse"
	TABLE: ClassVar[str] = "warehouses"

	id: int
	address: str
	description: str | None
	deleted_by: int | None
	deleted_at: datetime | None
	created_by: int | None
	created_at: datetime
