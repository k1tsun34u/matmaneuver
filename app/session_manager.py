from flask import redirect, request
from functools import wraps
from app.config import Config
from datetime import timedelta
from app.errors.mapper import Mapper
from app.services.employees_service import EmployeesService
from app.types.token_payload import TokenPayload
from app.services.users_service import UsersService
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


def require_session(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		auth_header = request.headers.get('Authorization')
		if auth_header is not None and auth_header.startswith('Bearer '):
			parts = auth_header.split(" ", 1)
			if len(parts) != 2:
				return redirect('/login')
				# return Mapper.router_error("Недействительная сессия!", 401)
			
			session = auth_header.split(' ')[1]
			try:
				token = SessionManager.decompose_token(session)
				tmp = UsersService.get_by_id(token.user_id)
				if tmp.error:
					return Mapper.error(tmp.error)
				
				user = tmp.result
				if user.token_ver != token.token_ver:
					return redirect('/login')
					# return Mapper.router_error("Сессия устарела! Выполните повторный вход", 401)
				
				return func(user, token, *args, **kwargs)
			except InvalidValueError:
				return redirect('/login')
				# return Mapper.router_error("Недействительная сессия!", 401)
		return redirect('/login')
		# return Mapper.router_error("Требуется авторизация!", 401)
	return wrapper

def require_employee_session(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		auth_header = request.headers.get('Authorization')
		if auth_header is not None and auth_header.startswith('Bearer '):
			parts = auth_header.split(" ", 1)
			if len(parts) != 2:
				return redirect('/login')
				#return Mapper.router_error("Недействительная сессия!", 401)
			
			session = auth_header.split(' ')[1]
			try:
				token = SessionManager.decompose_token(session)
				tmp = UsersService.get_by_id(token.user_id)
				if tmp.error:
					return redirect('/login')
					#return Mapper.error(tmp.error)
				
				user = tmp.result
				if user.token_ver != token.token_ver:
					return redirect('/login')
					# return Mapper.router_error("Сессия устарела! Выполните повторный вход", 401)
				
				tmp = EmployeesService.get_by_user_id(user_id=user.id)
				if tmp.error:
					return Mapper.router_error('Вы не сотрудник!', 400)
				
				employee_id = tmp.result.id
				return func(user, token, employee_id, *args, **kwargs)
			except InvalidValueError:
				return redirect('/login')
				# return Mapper.router_error("Недействительная сессия!", 401)
		return redirect('/login')
		# return Mapper.router_error("Требуется авторизация!", 401)
	return wrapper
