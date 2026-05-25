from typing import ClassVar
from decimal import Decimal
from datetime import datetime
from dataclasses import dataclass
from app.models.public.base_model import BaseModel

@dataclass
class Product(BaseModel):
	COLUMN_ID: ClassVar[str] = "id"
	COLUMN_NAME: ClassVar[str] = "name"
	COLUMN_DESCRIPTION: ClassVar[str] = "description"
	COLUMN_PRICE: ClassVar[str] = "price"
	COLUMN_DELETED_BY: ClassVar[str] = "deleted_by"
	COLUMN_DELETED_AT: ClassVar[str] = "deleted_at"
	COLUMN_CREATED_BY: ClassVar[str] = "created_by"
	COLUMN_CREATED_AT: ClassVar[str] = "created_at"

	TABLE: ClassVar[str] = "products"
	ENTITY: ClassVar[str] = "Product"

	id: int
	name: str
	description: str | None
	price: Decimal
	deleted_by: int | None
	deleted_at: datetime | None
	created_by: int | None
	created_at: datetime
