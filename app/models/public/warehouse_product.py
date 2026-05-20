from datetime import datetime
from dataclasses import dataclass
from app.models.public.base_model import BaseModel

@dataclass
class WarehouseProduct(BaseModel):
	product_id: int
	warehouse_id: int
	quantity: int
	reserved_quantity: int

	created_by: int | None
	created_at: datetime