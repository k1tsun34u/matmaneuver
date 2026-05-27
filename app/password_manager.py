import bcrypt


class PasswordManager:
	@classmethod
	def hash_password(cls, password: str) -> str:
		return bcrypt.hashpw(
			password.encode("utf-8"),
			bcrypt.gensalt()
		).decode("utf-8")
	
	@classmethod
	def verify_password(cls, password: str, password_hash: str) -> bool:
		try:
			return bcrypt.checkpw(
				password.encode("utf-8"),
				password_hash.encode("utf-8")
			)
		except Exception:
			return False
