from typing import ClassVar
from decimal import Decimal
from datetime import datetime
from dataclasses import dataclass
from app.types.payment_method import PaymentMethod
from app.models.public.base_model import BaseModel

@dataclass
class OrderPayment(BaseModel):
	COLUMN_ID: ClassVar[str] = "id"
	COLUMN_ORDER_ID: ClassVar[str] = "order_id"
	COLUMN_AMOUNT: ClassVar[str] = "amount"
	COLUMN_PAYMENT_METHOD: ClassVar[str] = "payment_method"
	COLUMN_CREATED_AT: ClassVar[str] = "created_at"

	TABLE: ClassVar[str] = "order_payments"
	ENTITY: ClassVar[str] = "OrderPayment"

	id: int
	order_id: int
	amount: Decimal
	payment_method: PaymentMethod
	created_at: datetime
