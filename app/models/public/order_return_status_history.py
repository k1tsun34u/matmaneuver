from datetime import datetime
from dataclasses import dataclass
from app.types.return_status import ReturnStatus
from app.models.public.base_model import BaseModel

@dataclass
class OrderReturnStatusHistory(BaseModel):
	id: int
	order_return_id: int
	status: ReturnStatus
	changed_by: int | None
	changed_at: datetime
