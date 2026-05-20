from datetime import datetime
from dataclasses import dataclass
from app.types.supply_status import SupplyStatus
from app.models.public.base_model import BaseModel

@dataclass
class SupplyStatusHistory(BaseModel):
	id: int
	supply_id: int
	status: SupplyStatus
	changed_by: int | None
	changed_at: datetime