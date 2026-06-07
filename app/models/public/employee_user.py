from datetime import datetime
from dataclasses import dataclass

@dataclass
class EmployeeUser:
	id: int
	user_id: int
	hired_by: int | None
	hired_at: datetime | None
	fired_by: int | None
	fired_at: datetime | None
	created_by: int | None
	created_at: datetime

	phone: str
	email: str | None
	full_name: str

	fired_by_full_name: str | None
	hired_by_full_name: str | None
