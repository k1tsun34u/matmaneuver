from decimal import Decimal
from dataclasses import dataclass
from app.models.public.base_model import BaseModel

@dataclass
class OrderReturnItem(BaseModel):
	id: int
	order_return_id: int
	order_item_id: int
	quantity: int
	price: Decimal
