from dataclasses import dataclass
from datetime import date, datetime
from app.types.supply_status import SupplyStatus

@dataclass
class ResponseSupply:
	id: int
	supplier_id: int
	warehouse_id: int
	current_status: SupplyStatus
	planned_delivery_date: date
	created_by: int | None
	created_at: datetime
