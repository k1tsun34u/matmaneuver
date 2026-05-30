from datetime import datetime
from dataclasses import dataclass
from app.models.public.category import Category


@dataclass
class ResponseCategory:
	id: int
	parent_category_id: int | None
	name: str
	deactivated_at: datetime | None

	def __init__(self, category: Category):
		self.id = category.id
		self.parent_category_id = category.parent_category_id
		self.name = category.name
		self.deactivated_at = category.deactivated_at
