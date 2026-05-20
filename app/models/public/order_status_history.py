from datetime import datetime
from dataclasses import dataclass
from app.types.order_status import OrderStatus
from app.models.public.base_model import BaseModel

@dataclass
class OrderStatusHistory(BaseModel):
	id: int
	order_id: int
	status: OrderStatus
	
	changed_by: int | None
	"""users(id)"""

	changed_at: datetime