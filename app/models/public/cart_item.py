from typing import ClassVar
from datetime import datetime
from dataclasses import dataclass
from app.models.public.base_model import BaseModel

@dataclass
class CartItem(BaseModel):
	COLUMN_CART_ID: ClassVar[str] = "cart_id"
	COLUMN_PRODUCT_ID: ClassVar[str] = "product_id"
	COLUMN_QUANTITY: ClassVar[str] = "quantity"
	COLUMN_CREATED_AT: ClassVar[str] = "created_at"

	TABLE: ClassVar[str] = "cart_items"
	ENTITY: ClassVar[str] = "CartItem"
	
	cart_id: int
	product_id: int
	quantity: int
	created_at: datetime
