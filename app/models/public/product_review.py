from typing import ClassVar
from datetime import datetime
from dataclasses import dataclass
from app.models.public.base_model import BaseModel

@dataclass
class ProductReview(BaseModel):
	COLUMN_PRODUCT_ID: ClassVar[str] = "product_id"
	COLUMN_USER_ID: ClassVar[str] = "user_id"
	COLUMN_RATING: ClassVar[str] = "rating"
	COLUMN_COMMENT: ClassVar[str] = "comment"
	COLUMN_CREATED_AT: ClassVar[str] = "created_at"

	TABLE: ClassVar[str] = "product_reviews"
	ENTITY: ClassVar[str] = "ProductReview"

	product_id: int
	user_id: int
	rating: int
	comment: str | None
	created_at: datetime
