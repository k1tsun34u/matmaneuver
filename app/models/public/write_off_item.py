from typing import ClassVar
from decimal import Decimal
from dataclasses import dataclass
from app.models.public.base_model import BaseModel

@dataclass
class WriteOffItem(BaseModel):
	COLUMN_ID: ClassVar[str] = "id"
	COLUMN_WRITE_OFF_ID: ClassVar[str] = "write_off_id"
	COLUMN_PRODUCT_ID: ClassVar[str] = "product_id"
	COLUMN_QUANTITY: ClassVar[str] = "quantity"
	COLUMN_PRICE: ClassVar[str] = "price"

	TABLE: ClassVar[str] = "write_off_items"
	ENTITY: ClassVar[str] = "WriteOffItem"
	
	id: int
	write_off_id: int
	product_id: int
	quantity: int
	price: Decimal
