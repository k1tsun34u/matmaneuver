from typing import ClassVar
from datetime import datetime
from dataclasses import dataclass
from app.types.order_status import OrderStatus
from app.models.public.base_model import BaseModel

@dataclass
class Order(BaseModel):
	COLUMN_ID: ClassVar[str] = "id"
	COLUMN_CURRENT_STATUS: ClassVar[str] = "current_status"
	COLUMN_TRACK_NUMBER: ClassVar[str] = "track_number"
	COLUMN_DELIVERY_ADDRESS: ClassVar[str] = "delivery_address"
	COLUMN_CREATED_BY: ClassVar[str] = "created_by"
	COLUMN_CREATED_AT: ClassVar[str] = "created_at"

	TABLE: ClassVar[str] = "orders"
	ENTITY: ClassVar[str] = "Order"

	id: int
	current_status: OrderStatus
	track_number: str
	delivery_address: str
	created_by: int
	created_at: datetime
