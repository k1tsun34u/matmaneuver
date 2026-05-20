from decimal import Decimal
from dataclasses import dataclass
from app.models.public.base_model import BaseModel

@dataclass
class SupplyItem(BaseModel):
	id: int
	supply_id: int
	product_id: int
	quantity: int
	price: Decimal