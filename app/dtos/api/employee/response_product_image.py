from datetime import datetime
from dataclasses import dataclass

@dataclass
class ResponseProductImage:
	id: int
	product_id: int
	storage_key: str
	created_by: int | None
	created_at: datetime
