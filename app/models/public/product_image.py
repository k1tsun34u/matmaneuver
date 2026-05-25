from typing import ClassVar
from datetime import datetime
from dataclasses import dataclass
from app.models.public.base_model import BaseModel

@dataclass
class ProductImage(BaseModel):
	COLUMN_ID: ClassVar[str] = "id"
	COLUMN_PRODUCT_ID: ClassVar[str] = "product_id"
	COLUMN_STORAGE_KEY: ClassVar[str] = "storage_key"
	COLUMN_CREATED_BY: ClassVar[str] = "created_by"
	COLUMN_CREATED_AT: ClassVar[str] = "created_at"

	TABLE: ClassVar[str] = "product_images"
	ENTITY: ClassVar[str] = "ProductImage"

	id: int
	product_id: int
	storage_key: str
	created_by: int | None
	created_at: datetime
