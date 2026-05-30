from decimal import Decimal
from datetime import datetime
from dataclasses import dataclass
from app.models.public.product import Product


@dataclass
class ResponseProduct:
	id: int
	name: str
	description: str | None
	price: Decimal
	deleted_at: datetime

	def __init__(self, product: Product):
		self.id = product.id
		self.name = product.name
		self.description = product.description
		self.price = product.price
		self.deleted_at = product.deleted_at
