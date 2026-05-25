from typing import ClassVar
from datetime import datetime
from dataclasses import dataclass
from app.types.supply_status import SupplyStatus
from app.models.public.base_model import BaseModel

@dataclass
class SupplyStatusHistory(BaseModel):
	COLUMN_ID: ClassVar[str] = "id"
	COLUMN_SUPPLY_ID: ClassVar[str] = "supply_id"
	COLUMN_STATUS: ClassVar[str] = "status"
	COLUMN_CHANGED_BY: ClassVar[str] = "changed_by"
	COLUMN_CHANGED_AT: ClassVar[str] = "changed_at"

	TABLE: ClassVar[str] = "supply_status_history"
	ENTITY: ClassVar[str] = "SupplyStatusHistory"

	id: int
	supply_id: int
	status: SupplyStatus
	changed_by: int | None
	changed_at: datetime
