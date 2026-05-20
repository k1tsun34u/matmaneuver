from decimal import Decimal
from datetime import datetime
from dataclasses import dataclass
from app.models.public.base_model import BaseModel

@dataclass
class Product(BaseModel):
	id: int
	name: str
	description: str | None
	price: Decimal

	deleted_by: int | None
	"""users(id)"""

	deleted_at: datetime | None

	created_by: int | None
	"""users(id)"""

	created_at: datetime
