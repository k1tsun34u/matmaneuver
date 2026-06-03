from decimal import Decimal
from dataclasses import dataclass

@dataclass
class ResponseWriteOffItem:
	id: int
	write_off_id: int
	product_id: int
	quantity: int
	price: Decimal
