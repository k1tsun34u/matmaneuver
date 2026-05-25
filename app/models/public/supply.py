from typing import ClassVar
from dataclasses import dataclass
from datetime import date, datetime
from app.types.supply_status import SupplyStatus
from app.models.public.base_model import BaseModel

@dataclass
class Supply(BaseModel):
	COLUMN_ID: ClassVar[str] = "id"
	COLUMN_SUPPLIER_ID: ClassVar[str] = "supplier_id"
	COLUMN_WAREHOUSE_ID: ClassVar[str] = "warehouse_id"
	COLUMN_CURRENT_STATUS: ClassVar[str] = "current_status"
	COLUMN_PLANNED_DELIVERY_DATE: ClassVar[str] = "planned_delivery_date"
	COLUMN_CREATED_BY: ClassVar[str] = "created_by"
	COLUMN_CREATED_AT: ClassVar[str] = "created_at"

	TABLE: ClassVar[str] = "supplies"
	ENTITY: ClassVar[str] = "Supply"

	id: int
	supplier_id: int
	warehouse_id: int
	current_status: SupplyStatus
	planned_delivery_date: date
	created_by: int | None
	created_at: datetime
