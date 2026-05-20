from dataclasses import dataclass
from datetime import datetime
from app.models.public.base_model import BaseModel

@dataclass
class ProductImage(BaseModel):
	id: int
	product_id: int
	storage_key: str

	created_by: int | None
	"""users(id)"""

	created_at: datetime