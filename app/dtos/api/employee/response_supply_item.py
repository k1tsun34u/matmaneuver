from decimal import Decimal
from dataclasses import dataclass

@dataclass
class ResponseSupplyItem:
	id: int
	supply_id: int
	product_id: int
	quantity: int
	price: Decimal
