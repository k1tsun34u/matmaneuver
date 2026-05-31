from datetime import datetime
from dataclasses import dataclass
from app.models.public.product_review import ProductReview


@dataclass
class ResponseProductReview:
	product_id: int
	user_id: int
	rating: int
	comment: str | None

	def __init__(self, product_review: ProductReview):
		self.product_id = product_review.product_id
		self.user_id = product_review.user_id
		self.rating = product_review.rating
		self.comment = product_review.comment
