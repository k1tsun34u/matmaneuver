from datetime import datetime
from dataclasses import dataclass

@dataclass
class ResponseWarehouse:
	id: int
	address: str
	description: str | None
	deleted_by: int | None
	deleted_at: datetime | None
	created_by: int | None
	created_at: datetime
