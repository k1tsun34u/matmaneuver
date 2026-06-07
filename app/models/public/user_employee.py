from datetime import datetime
from dataclasses import dataclass

@dataclass
class UserEmployee:
	id: int
	phone: str
	email: str | None
	full_name: str
	password_hash: str
	token_ver: int

	blocked_by: int | None
	blocked_at: datetime | None

	deleted_by: int | None
	deleted_at: datetime | None

	created_by: int | None
	created_at: datetime

	blocked_by_full_name: str | None
	deleted_by_full_name: str | None
