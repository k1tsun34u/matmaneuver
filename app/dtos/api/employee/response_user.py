from datetime import datetime
from dataclasses import dataclass


@dataclass
class ResponseUser:
	id: int
	phone: str
	email: str
	full_name: str
	blocked_by: int | None
	blocked_at: datetime
	deleted_by: int | None
	deleted_at: datetime | None
	created_by: int | None
	created_at: datetime
