from app.errors.base_error import BaseError


class AlreadyExistsError(BaseError):
	def __init__(self, entity: str, field: str):
		self.entity = entity.capitalize()
		self.field = field

	def __repr__(self):
		return f"AlreadyExistsError('{self.entity}', '{self.field}')"
