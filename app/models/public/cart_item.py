from datetime import datetime
from dataclasses import dataclass
from app.models.public.base_model import BaseModel

@dataclass
class CartItem(BaseModel):
	cart_id: int
	product_id: int
	quantity: int
	created_at: datetime
