from datetime import datetime
from dataclasses import dataclass

@dataclass
class SupplierEmployee:
	id: int
	full_name: str
	phone: str
	email: str | None
	address: str | None
	deactivated_by: int | None
	deactivated_at: datetime | None
	created_by: int | None
	created_at: datetime

	deactivated_by_full_name: str | None
