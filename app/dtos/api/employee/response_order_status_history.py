from datetime import datetime
from dataclasses import dataclass
from app.types.order_status import OrderStatus

@dataclass
class ResponseOrderStatusHistory:
	id: int
	order_id: int
	status: OrderStatus
	changed_by: int | None
	changed_at: datetime
