from datetime import datetime
from dataclasses import dataclass
from app.types.supply_status import SupplyStatus

@dataclass
class ResponseSupplyStatusHistory:
	id: int
	supply_id: int
	status: SupplyStatus
	changed_by: int | None
	changed_at: datetime
