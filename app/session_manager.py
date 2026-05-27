from app.config import Config
from datetime import timedelta
from app.types.token_payload import TokenPayload
from app.errors.invalid_value_error import InvalidValueError
from itsdangerous import URLSafeTimedSerializer, BadData, SignatureExpired


class SessionManager:
	SERIALIZER = URLSafeTimedSerializer(Config.SECRET_KEY, salt="auth-token")
	EXPIRED_AFTER = timedelta(days=30)

	KEY_UID = "uid"
	KEY_VER = "ver"

	@classmethod
	def compose_token(cls, user_id: int, token_ver: int) -> str:
		return cls.SERIALIZER.dumps({
			cls.KEY_UID: user_id,
			cls.KEY_VER: token_ver
		})
	
	@classmethod
	def decompose_token(cls, token: str) -> TokenPayload:
		try:
			decomposed = cls.SERIALIZER.loads(token, max_age=int(cls.EXPIRED_AFTER.total_seconds()))
			if not isinstance(decomposed, dict):
				raise InvalidValueError("Session", "value")

			user_id = decomposed.get(cls.KEY_UID)
			token_ver = decomposed.get(cls.KEY_VER)
			if not (isinstance(user_id, int) and isinstance(token_ver, int)):
				raise InvalidValueError("Session", "value")
			
			return TokenPayload(user_id=user_id, token_ver=token_ver)
		except SignatureExpired:
			raise InvalidValueError("Session", "expired")
		except BadData:
			raise InvalidValueError("Session", "format")
