from datetime import datetime
from dataclasses import dataclass

@dataclass
class ResponseWarehouseProduct:
	product_id: int
	warehouse_id: int
	quantity: int
	reserved_quantity: int
	created_by: int | None
	created_at: datetime
