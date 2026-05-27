from functools import wraps
from app.unset import UNSET
from dataclasses import asdict
from app.errors.mapper import Mapper
from app.session_manager import SessionManager
from flask import Blueprint, request, jsonify
from app.password_manager import PasswordManager
from app.services.users_service import UsersService
from app.errors.invalid_value_error import InvalidValueError


client_auth_bp = Blueprint(
	"api_client_auth",
	__name__,
	url_prefix="/api/client/auth"
)

def require_session(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		if not request.json or "session" not in request.json:
			return Mapper.internal_server_error()
		try:
			token = SessionManager.decompose_token(request.json["session"])
			tmp = UsersService.get_by_id(token.user_id)
			if tmp.error:
				return Mapper.error(tmp.error)
			
			user = tmp.result
			if user.token_ver != token.token_ver:
				return Mapper.router_error("Сессия устарела! Выполните повторный вход", 401)
			
			return func(user, token, *args, **kwargs)
		except InvalidValueError:
			return Mapper.internal_server_error()
	return wrapper

@client_auth_bp.post("/register")
def register():
	data = request.get_json()
	required_fields = ("phone", "email", "full_name", "password",)
	if not data or not all(field in data for field in required_fields):
		return Mapper.internal_server_error()

	res = UsersService.register(
		phone=data["phone"],
		email=data["email"],
		full_name=data["full_name"],
		password_hash=PasswordManager.hash_password(data["password"]),
		created_by=None
	)

	if res.error:
		return Mapper.error(res.error)
	
	return jsonify({
		"success": True,
		"session": SessionManager.compose_token(res.result, 1)
	}), 201

@client_auth_bp.post("/login")
def login():
	data = request.get_json()
	if data and "password" in data:
		if "phone" in data:
			res = UsersService.get_by_phone(data["phone"])
			if res.error:
				return Mapper.error(res.error)
			
			user = res.result
			if not PasswordManager.verify_password(data["password"], user.password_hash):
				return Mapper.router_error("Неверный пароль!", 401)
			
			return jsonify({
				"success": True,
				"session": SessionManager.compose_token(user.id, user.token_ver)
			}), 200
		elif "email" in data:
			res = UsersService.get_by_email(data["email"])
			if res.error:
				return Mapper.error(res.error)
			
			user = res.result
			if not PasswordManager.verify_password(data["password"], user.password_hash):
				return Mapper.router_error("Неверный пароль!", 401)
			
			return jsonify({
				"success": True,
				"session": SessionManager.compose_token(user.id, user.token_ver)
			}), 200
	
	return Mapper.internal_server_error()

@client_auth_bp.post("/me")
@require_session
def me(user, _):
	return jsonify(asdict(user)), 200

@client_auth_bp.post("/update")
@require_session
def update(_, token):
	data = request.get_json()
	phone, email, full_name = UNSET, UNSET, UNSET
	if "phone" in data: phone = data["phone"]
	if "email" in data: email = data["email"]
	if "full_name" in data: full_name = data["full_name"]

	if not any((phone, email, full_name,)):
		return '', 200
	
	res = UsersService.update(
		token=token,
		phone=phone,
		email=email,
		full_name=full_name
	)

	if res.error:
		return Mapper.error(res.error)
	return '', 200

@client_auth_bp.post("/set-password")
@require_session
def set_password(_, token):
	data = request.get_json()
	res = UsersService.set_password(
		token=token,
		password_hash=PasswordManager.hash_password(data["password"])
	)

	if res.error:
		return Mapper.error(res.error)
	return '', 200
