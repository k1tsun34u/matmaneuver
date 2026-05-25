from typing import ClassVar
from datetime import datetime
from dataclasses import dataclass
from app.models.public.base_model import BaseModel
from app.types.write_off_reason import WriteOffReason

@dataclass
class WriteOff(BaseModel):
	COLUMN_ID: ClassVar[str] = "id"
	COLUMN_WAREHOUSE_ID: ClassVar[str] = "warehouse_id"
	COLUMN_REASON: ClassVar[str] = "reason"
	COLUMN_COMMENT: ClassVar[str] = "comment"
	COLUMN_CREATED_BY: ClassVar[str] = "created_by"
	COLUMN_CREATED_AT: ClassVar[str] = "created_at"

	TABLE: ClassVar[str] = "write_offs"
	ENTITY: ClassVar[str] = "WriteOff"

	id: int
	warehouse_id: int
	reason: WriteOffReason
	comment: str | None
	created_by: int | None
	created_at: datetime
