from app.utils import Utils
from dataclasses import asdict
from app.errors.mapper import Mapper
from app.types.cart_type import CartType
from flask import Blueprint, request, jsonify
from app.password_manager import PasswordManager
from app.services.users_service import UsersService
from app.services.carts_service import CartsService
from app.dtos.api.client.response_user import ResponseUser
from app.errors.already_exists_error import AlreadyExistsError
from app.session_manager import SessionManager, require_session


client_auth_bp = Blueprint(
	"api_client_auth",
	__name__,
	url_prefix="/api/client/auth"
)
	
@client_auth_bp.post("/login")
def login():
	data = request.get_json()
	phone = Utils.parse_str_from_dict(data, "phone")
	email = Utils.parse_str_from_dict(data, "email")
	password = Utils.parse_str_from_dict(data, "password")

	if password is not None:
		if phone is not None:
			res = UsersService.get_by_phone(phone)
			if res.error:
				return Mapper.error(res.error)
			
			user = res.result
			if not PasswordManager.verify_password(password, user.password_hash):
				return Mapper.router_error("Неверный пароль!", 401)
			
			return jsonify({
				"success": True,
				"session": SessionManager.compose_token(user.id, user.token_ver)
			}), 200
		elif email is not None:
			res = UsersService.get_by_email(email)
			if res.error:
				return Mapper.error(res.error)
			
			user = res.result
			if not PasswordManager.verify_password(password, user.password_hash):
				return Mapper.router_error("Неверный пароль!", 401)
			
			return jsonify({
				"success": True,
				"session": SessionManager.compose_token(user.id, user.token_ver)
			}), 200
	return Mapper.router_error("Неверный запрос", 400)

@client_auth_bp.post("/register")
def register():
	data = request.get_json()
	phone = Utils.parse_str_from_dict(data, "phone")
	email = Utils.parse_str_from_dict(data, "email")
	full_name = Utils.parse_str_from_dict(data, "full_name")
	password = Utils.parse_str_from_dict(data, "password")

	if all((phone, full_name, password,)):
		res = UsersService.register(
			phone=phone,
			email=email,
			full_name=full_name,
			password_hash=PasswordManager.hash_password(password),
			created_by=None
		)

		if res.error:
			return Mapper.error(res.error)
		
		user_id = res.result
		tmp = CartsService.create(
			user_id=user_id,
			type=CartType.ACTIVE
		)
		if tmp.error and not isinstance(tmp.error, AlreadyExistsError):
			return Mapper.error(tmp.error)
		
		tmp = CartsService.create(
			user_id=user_id,
			type=CartType.WISHLIST
		)
		if tmp.error and not isinstance(tmp.error, AlreadyExistsError):
			return Mapper.error(tmp.error)
		
		session = SessionManager.compose_token(user_id, 1)
		return jsonify({
			"success": True,
			"session": session
		}), 201
	return Mapper.router_error("Неверный запрос", 400)

@client_auth_bp.post("/update")
@require_session
def update(_, token):
	data = request.get_json()
	phone = Utils.parse_str_from_dict(data, "phone")
	email = Utils.parse_str_from_dict(data, "email")
	full_name = Utils.parse_str_from_dict(data, "full_name")

	if any((phone, email, full_name,)):
		res = UsersService.update(
			token=token,
			phone=Utils.value_for_update(phone),
			email=Utils.value_for_update(email),
			full_name=Utils.value_for_update(full_name)
		)

		if res.error:
			return Mapper.error(res.error)
	return jsonify({"success": True}), 200

@client_auth_bp.post("/set-password")
@require_session
def set_password(_, token):
	data = request.get_json()
	password = Utils.parse_str_from_dict(data, "password")

	if password is None:
		return Mapper.router_error("Неверный запрос", 400)

	res = UsersService.set_password(
		token=token,
		password_hash=PasswordManager.hash_password(password)
	)

	if res.error:
		return Mapper.error(res.error)
	
	return jsonify({
		"success": True,
		"session": res.result
	}), 200

@client_auth_bp.post("/me")
@require_session
def me(user, _):
	return jsonify({
		"success": True,
		"user": asdict(ResponseUser(user))
	}), 200
