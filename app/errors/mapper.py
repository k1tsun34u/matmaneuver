from flask import Response, jsonify
from app.errors.base_error import BaseError
from app.errors.not_found_error import NotFoundError
from app.errors.invalid_value_error import InvalidValueError
from app.errors.already_exists_error import AlreadyExistsError
from app.models.db.db_user import DbUser


class Mapper:
	@classmethod
	def error(cls, error: BaseError) -> tuple[Response, str]:
		if isinstance(error, InvalidValueError):
			return cls.invalid_value_error(error)
		if isinstance(error, NotFoundError):
			return cls.not_found_error(error)
		if isinstance(error, AlreadyExistsError):
			return cls.already_exists_error(error)

		return jsonify({
			"success": False,
			"error": "Внутренняя ошибка сервера"
		}), 400
	
	@classmethod
	def invalid_value_error(cls, error: InvalidValueError) -> tuple[Response, str]:
		match error.entity:
			case DbUser.ENTITY:
				match error.column:
					case DbUser.COLUMN_PHONE:
						return Mapper.router_error("Неверный номер телефона!", 400)
					case DbUser.COLUMN_EMAIL:
						return Mapper.router_error("Неверная почта!", 400)
					case DbUser.COLUMN_FULL_NAME:
						return Mapper.router_error("Неверное полное имя!", 400)
					case DbUser.COLUMN_PASSWORD_HASH:
						return Mapper.router_error("Неверный пароль!", 400)
		return cls.internal_server_error()
	
	@classmethod
	def not_found_error(cls, error: NotFoundError) -> tuple[Response, str]:
		match error.entity:
			case DbUser.ENTITY:
				match error.column:
					case DbUser.COLUMN_ID:
						return Mapper.router_error("Пользователь не найден!", 401)
					case DbUser.COLUMN_PHONE:
						return Mapper.router_error("Пользователь с таким номером не найден!", 401)
					case DbUser.COLUMN_EMAIL:
						return Mapper.router_error("Пользователь с такой почтой не найден!", 401)
		return cls.internal_server_error()
	
	@classmethod
	def already_exists_error(cls, error: AlreadyExistsError) -> tuple[Response, str]:
		match error.entity:
			case DbUser.ENTITY:
				match error.column:
					case DbUser.COLUMN_PHONE:
						return Mapper.router_error("Пользователь с таким номером уже существует!", 409)
					case DbUser.COLUMN_EMAIL:
						return Mapper.router_error("Пользователь с такой почтой уже существует!", 409)
		return cls.internal_server_error()

	@staticmethod
	def router_error(message: str, code: int) -> tuple[Response, str]:
		return jsonify({
			"success": False,
			"error": message
		}), code
	
	@classmethod
	def internal_server_error(cls) -> tuple[Response, str]:
		return cls.router_error("Внутренняя ошибка сервера!", 500)
