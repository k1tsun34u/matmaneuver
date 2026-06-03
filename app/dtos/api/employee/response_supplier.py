from datetime import datetime
from dataclasses import dataclass

@dataclass
class ResponseSupplier:
	id: int
	full_name: str
	phone: str
	email: str | None
	address: str | None
	deactivated_by: int | None
	deactivated_at: datetime | None
	created_by: int | None
	created_at: datetime
