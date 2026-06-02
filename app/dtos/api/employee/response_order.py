from datetime import datetime
from dataclasses import dataclass
from app.models.public.order import Order
from app.types.order_status import OrderStatus


@dataclass
class ResponseOrder:
	id: int
	current_status: OrderStatus
	track_number: str
	delivery_address: str
	created_by: int
	created_at: datetime
