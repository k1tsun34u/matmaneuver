from datetime import datetime
from dataclasses import dataclass


@dataclass
class ResponseCategory:
	id: int
	parent_category_id: int | None
	name: str
	deactivated_by: int | None
	deactivated_at: datetime | None
	created_by: int | None
	created_at: datetime
