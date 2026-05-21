

class InvalidTokenError(Exception):
	def __init__(self):
		super().__init__("Invalid token")


class ExpiredTokenError(Exception):
	def __init__(self, token: str):
		self.token = token
		super().__init__(f"Expired token: {token}")


class InvalidPhoneError(Exception):
	def __init__(self, phone: str):
		self.phone = phone
		super().__init__(f"Invalid phone: {phone}")
		

class InvalidEmailError(Exception):
	def __init__(self, email: str):
		self.email = email
		super().__init__(f"Invalid email: {email}")


class InvalidFullNameError(Exception):
	def __init__(self, full_name: str):
		self.full_name = full_name
		super().__init__(f"Invalid full name: {full_name}")


class InvalidPasswordHashError(Exception):
	def __init__(self, password_hash: str):
		self.password_hash = password_hash
		super().__init__(f"Invalid password hash: {password_hash}")


class InvalidCodeError(Exception):
	def __init__(self, code: str):
		self.code = code
		super().__init__(f"Invalid code: {code}")
