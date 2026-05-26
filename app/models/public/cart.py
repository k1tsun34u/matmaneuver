from typing import ClassVar
from datetime import datetime
from dataclasses import dataclass
from app.types.cart_type import CartType
from app.models.public.base_model import BaseModel

@dataclass
class Cart(BaseModel):
	COLUMN_ID: ClassVar[str] = "id"
	COLUMN_USER_ID: ClassVar[str] = "user_id"
	COLUMN_TYPE: ClassVar[str] = "type"
	COLUMN_CREATED_AT: ClassVar[str] = "created_at"

	TABLE: ClassVar[str] = "carts"
	ENTITY: ClassVar[str] = "Cart"

	id: int
	user_id: int
	type: CartType
	created_at: datetime
