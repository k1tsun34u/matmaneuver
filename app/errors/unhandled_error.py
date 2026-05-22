from app.errors.base_error import BaseError


class UnhandledError(BaseError):
	def __init__(self, message: str):
		self.message = message

	def __repr__(self):
		return f"UnhandledError('{self.message}')"
