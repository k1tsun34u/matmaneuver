from datetime import datetime
from dataclasses import dataclass


@dataclass
class ResponseProductReview:
	product_id: int
	user_id: int
	rating: int
	comment: str | None
	created_at: datetime
