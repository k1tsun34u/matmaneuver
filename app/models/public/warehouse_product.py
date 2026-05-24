from typing import ClassVar
from datetime import datetime
from dataclasses import dataclass
from app.models.public.base_model import BaseModel

@dataclass
class WarehouseProduct(BaseModel):
	COLUMN_PRODUCT_ID: ClassVar[str] = "product_id"
	COLUMN_WAREHOUSE_ID: ClassVar[str] = "warehouse_id"
	COLUMN_QUANTITY: ClassVar[str] = "quantity"
	COLUMN_RESERVED_QUANTITY: ClassVar[str] = "reserved_quantity"
	COLUMN_CREATED_BY: ClassVar[str] = "created_by"
	COLUMN_CREATED_AT: ClassVar[str] = "created_at"

	ENTITY: ClassVar[str] = "WarehouseProduct"
	TABLE: ClassVar[str] = "warehouse_products"

	product_id: int
	warehouse_id: int
	quantity: int
	reserved_quantity: int
	created_by: int | None
	created_at: datetime
