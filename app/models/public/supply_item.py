from typing import ClassVar
from decimal import Decimal
from dataclasses import dataclass
from app.models.public.base_model import BaseModel

@dataclass
class SupplyItem(BaseModel):
	COLUMN_ID: ClassVar[str] = "id"
	COLUMN_SUPPLY_ID: ClassVar[str] = "supply_id"
	COLUMN_PRODUCT_ID: ClassVar[str] = "product_id"
	COLUMN_QUANTITY: ClassVar[str] = "quantity"
	COLUMN_PRICE: ClassVar[str] = "price"

	TABLE: ClassVar[str] = "supply_items"
	ENTITY: ClassVar[str] = "SupplyItem"

	id: int
	supply_id: int
	product_id: int
	quantity: int
	price: Decimal
