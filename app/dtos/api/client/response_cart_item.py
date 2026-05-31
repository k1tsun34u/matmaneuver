from dataclasses import dataclass
from app.models.public.cart_item import CartItem


@dataclass
class ResponseCartItem:
	cart_id: int
	product_id: int
	quantity: int

	def __init__(self, cart_item: CartItem):
		self.cart_id = cart_item.cart_id
		self.product_id = cart_item.product_id
		self.quantity = cart_item.quantity
