from datetime import datetime
from dataclasses import dataclass

@dataclass
class ResponseProductCategory:
	product_id: int
	category_id: int

	assigned_by: int | None
	"""employees(id)"""

	assigned_at: datetime
