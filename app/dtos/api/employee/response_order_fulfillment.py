from datetime import datetime
from dataclasses import dataclass

@dataclass
class ResponseOrderFulfillment:
	id: int
	order_id: int
	warehouse_id: int
	created_at: datetime
