from datetime import datetime
from dataclasses import dataclass
from app.models.public.base_model import BaseModel
from app.types.write_off_reason import WriteOffReason

@dataclass
class WriteOff(BaseModel):
	id: int
	warehouse_id: int
	reason: WriteOffReason
	comment: str | None
	created_by: int | None
	created_at: datetime
