from datetime import datetime
from dataclasses import dataclass

@dataclass
class Role:
	id: int
	code: str
	is_system: bool
	deactivated_by: int | None
	deactivated_at: datetime | None
	created_by: int | None
	created_at: datetime
