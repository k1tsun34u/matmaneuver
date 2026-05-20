from datetime import datetime
from dataclasses import dataclass
from app.models.public.base_model import BaseModel

@dataclass
class ProductReview(BaseModel):
	product_id: int
	user_id: int
	rating: int
	comment: str | None
	created_at: datetime
