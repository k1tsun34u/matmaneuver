from typing import ClassVar
from datetime import datetime
from dataclasses import dataclass
from app.types.order_status import OrderStatus
from app.models.public.base_model import BaseModel

@dataclass
class OrderStatusHistory(BaseModel):
	COLUMN_ID: ClassVar[str] = "id"
	COLUMN_ORDER_ID: ClassVar[str] = "order_id"
	COLUMN_STATUS: ClassVar[str] = "status"
	COLUMN_CHANGED_BY: ClassVar[str] = "changed_by"
	COLUMN_CHANGED_AT: ClassVar[str] = "changed_at"

	TABLE: ClassVar[str] = "order_status_history"
	ENTITY: ClassVar[str] = "OrderStatusHistory"

	id: int
	order_id: int
	status: OrderStatus
	changed_by: int | None
	changed_at: datetime
