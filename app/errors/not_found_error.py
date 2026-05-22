from app.errors.base_error import BaseError


class NotFoundError(BaseError):
	def __init__(self, entity: str, field: str):
		self.entity = entity.capitalize()
		self.field = field

	def __repr__(self):
		return f"NotFoundError('{self.entity}', '{self.field}')"
