from app.errors.base_error import BaseError


class NotAllowedError(BaseError):
	def __init__(self, action: str, column: str | None):
		self.action = action
		self.column = column

	def __repr__(self):
		second_param = f"'{self.column}'" if self.column is not None else "None"
		return f"NotAllowedError('{self.action}', {second_param})"
