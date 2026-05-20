from dataclasses import dataclass
from datetime import datetime
from app.models.public.base_model import BaseModel

@dataclass
class OrderFulfillment(BaseModel):
	id: int
	order_id: int
	warehouse_id: int
	created_at: datetime
