from typing import ClassVar
from datetime import datetime
from dataclasses import dataclass
from app.models.public.base_model import BaseModel

@dataclass
class ProductCategory(BaseModel):
	COLUMN_PRODUCT_ID: ClassVar[str] = "product_id"
	COLUMN_CATEGORY_ID: ClassVar[str] = "category_id"
	COLUMN_ASSIGNED_BY: ClassVar[str] = "assigned_by"
	COLUMN_ASSIGNED_AT: ClassVar[str] = "assigned_at"

	TABLE: ClassVar[str] = "product_categories"
	ENTITY: ClassVar[str] = "ProductCategory"

	product_id: int
	category_id: int

	assigned_by: int | None
	"""employees(id)"""

	assigned_at: datetime
