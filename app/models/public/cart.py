from datetime import datetime
from dataclasses import dataclass
from app.types.cart_type import CartType
from app.models.public.base_model import BaseModel

@dataclass
class Cart(BaseModel):
	id: int
	user_id: int
	type: CartType
	created_at: datetime
