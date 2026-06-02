from decimal import Decimal
from dataclasses import dataclass

@dataclass
class ResponseOrderFulfillmentItem:
	id: int
	order_fulfillment_id: int
	product_id: int
	quantity: int
	price: Decimal
