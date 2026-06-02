from decimal import Decimal
from datetime import datetime
from dataclasses import dataclass
from app.types.payment_method import PaymentMethod

@dataclass
class ResponseOrderPayment:
	id: int
	order_id: int
	amount: Decimal
	payment_method: PaymentMethod
	created_at: datetime
