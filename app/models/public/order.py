from datetime import datetime
from dataclasses import dataclass
from app.types.order_status import OrderStatus
from app.models.public.base_model import BaseModel

@dataclass
class Order(BaseModel):
	id: int
	current_status: OrderStatus
	track_number: str
	delivery_address: str
	created_by: int
	created_at: datetime
