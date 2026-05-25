from typing import ClassVar
from decimal import Decimal
from dataclasses import dataclass
from app.models.public.base_model import BaseModel

@dataclass
class OrderItem(BaseModel):
	COLUMN_ID: ClassVar[str] = "id"
	COLUMN_ORDER_ID: ClassVar[str] = "order_id"
	COLUMN_PRODUCT_ID: ClassVar[str] = "product_id"
	COLUMN_QUANTITY: ClassVar[str] = "quantity"
	COLUMN_PRICE: ClassVar[str] = "price"

	TABLE: ClassVar[str] = "order_items"
	ENTITY: ClassVar[str] = "OrderItem"

	id: int
	order_id: int
	product_id: int
	quantity: int
	price: Decimal
