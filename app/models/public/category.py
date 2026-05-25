from typing import ClassVar
from datetime import datetime
from dataclasses import dataclass
from app.models.public.base_model import BaseModel

@dataclass
class Category(BaseModel):
	COLUMN_ID: ClassVar[str] = "id"
	COLUMN_PARENT_CATEGORY_ID: ClassVar[str] = "parent_category_id"
	COLUMN_NAME: ClassVar[str] = "name"
	COLUMN_DEACTIVATED_BY: ClassVar[str] = "deactivated_by"
	COLUMN_DEACTIVATED_AT: ClassVar[str] = "deactivated_at"
	COLUMN_CREATED_BY: ClassVar[str] = "created_by"
	COLUMN_CREATED_AT: ClassVar[str] = "created_at"

	TABLE: ClassVar[str] = "categories"
	ENTITY: ClassVar[str] = "Category"

	id: int
	parent_category_id: int | None
	name: str
	deactivated_by: int | None
	deactivated_at: datetime | None
	created_by: int | None
	created_at: datetime
