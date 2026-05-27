from app.errors.base_error import BaseError


class InvalidValueError(BaseError):
	def __init__(self, entity: str, field: str):
		self.entity = entity
		self.column = field

	def __repr__(self):
		return f"InvalidValueError('{self.entity}', '{self.column}')"
