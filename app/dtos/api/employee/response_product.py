from decimal import Decimal
from datetime import datetime
from dataclasses import dataclass

@dataclass
class ResponseProduct:
	id: int
	name: str
	description: str | None
	price: Decimal
	deleted_by: int | None
	deleted_at: datetime | None
	created_by: int | None
	created_at: datetime
