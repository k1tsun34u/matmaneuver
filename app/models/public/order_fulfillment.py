from typing import ClassVar
from datetime import datetime
from dataclasses import dataclass
from app.models.public.base_model import BaseModel

@dataclass
class OrderFulfillment(BaseModel):
	COLUMN_ID: ClassVar[str] = "id"
	COLUMN_ORDER_ID: ClassVar[str] = "order_id"
	COLUMN_WAREHOUSE_ID: ClassVar[str] = "warehouse_id"
	COLUMN_CREATED_AT: ClassVar[str] = "created_at"

	TABLE: ClassVar[str] = "order_fulfillments"
	ENTITY: ClassVar[str] = "OrderFulfillment"

	id: int
	order_id: int
	warehouse_id: int
	created_at: datetime
