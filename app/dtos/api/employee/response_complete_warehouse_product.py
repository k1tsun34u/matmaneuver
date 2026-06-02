from datetime import datetime
from dataclasses import dataclass

class ResponseCompleteWarehouseProduct:
	warehouse_id: int
	warehouse_address: str
	warehouse_description: str | None
	warehouse_deleted_by: int | None
	warehouse_deleted_at: datetime | None
	warehouse_created_by: int | None
	warehouse_created_at: datetime

	product_id: int
	product_quantity: int
	product_reserved_quantity: int
	product_created_by: int | None
	product_created_at: datetime
