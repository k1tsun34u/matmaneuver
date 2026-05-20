from datetime import datetime
from dataclasses import dataclass
from app.types.return_status import ReturnStatus
from app.models.public.base_model import BaseModel

@dataclass
class OrderReturn(BaseModel):
	id: int
	order_id: int
	reason: str
	current_status: ReturnStatus

	created_by: int
	"""users(id)"""


	created_at: datetime
