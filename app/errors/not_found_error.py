from app.errors.base_error import BaseError


class NotFoundError(BaseError):
	def __init__(self, entity: str, field: str | None = None):
		self.entity = entity.capitalize()
		self.field = field

	def __repr__(self):
		secondary = f"'{self.field}'" if self.field else ""
		return f"NotFoundError('{self.entity}', {secondary})"
