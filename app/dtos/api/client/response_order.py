from dataclasses import dataclass
from app.models.public.order import Order
from app.types.order_status import OrderStatus


@dataclass
class ResponseOrder:
	id: int
	current_status: OrderStatus
	track_number: str
	delivery_address: str

	def __init__(self, order: Order):
		self.id = order.id
		self.current_status = order.current_status
		self.track_number = order.track_number
		self.delivery_address = order.delivery_address
