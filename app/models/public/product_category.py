from dataclasses import dataclass
from datetime import datetime
from app.models.public.base_model import BaseModel

@dataclass
class ProductCategory(BaseModel):
	product_id: int
	category_id: int

	assigned_by: int | None
	"""users(id)"""

	assigned_at: datetime