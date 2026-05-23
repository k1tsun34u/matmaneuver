import psycopg
from app.utils import Utils
from app.unset import Unset, UNSET
from app.models.db.db_user import DbUser
from app.types.token_payload import TokenPayload
from app.services.base_service import BaseService
from app.types.service_result import ServiceResult
from app.errors.not_found_error import NotFoundError
from app.types.transaction_helper import TransactionHelper
from app.errors.invalid_value_error import InvalidValueError
from app.repositories.public.users_repository import UsersRepository


class UsersService(BaseService):
	ENTITY = "User"
	KEY_HELPERS = (TransactionHelper(ENTITY, "users", (
		DbUser.COLUMN_PHONE,
		DbUser.COLUMN_EMAIL,
	)),)

	FKEY_HELPERS = (TransactionHelper(ENTITY, "users", (
		DbUser.COLUMN_BLOCKED_BY,
		DbUser.COLUMN_DELETED_BY,
		DbUser.COLUMN_CREATED_BY,
	)),)

	MAX_PHONE_LENGTH = 32
	MAX_EMAIL_LENGTH = 256

	@classmethod
	def _normalize_fields_or_catch(
		cls,
		phone: str | Unset,
		email: str | None | Unset,
		full_name: str | Unset
	) -> tuple[str | Unset, str | None | Unset, str | Unset] | InvalidValueError:
		if not isinstance(phone, Unset):
			normalized_phone = Utils.normalize_phone(phone)
			is_valid_phone = (
				len(normalized_phone) <= cls.MAX_PHONE_LENGTH
				and Utils.is_valid_phone(normalized_phone)
			)

			if not is_valid_phone:
				return InvalidValueError(cls.ENTITY, DbUser.COLUMN_PHONE)
			
			phone = normalized_phone
		
		if not (isinstance(email, Unset) or email is None):
			normalized_email = Utils.normalize_email(email)
			is_valid_email = (
				len(normalized_email) <= cls.MAX_EMAIL_LENGTH
				and Utils.is_valid_email(normalized_email)
			)

			if not is_valid_email:
				return InvalidValueError(cls.ENTITY, DbUser.COLUMN_EMAIL)
			
			email = normalized_email
		
		if not isinstance(full_name, Unset):
			normalized_full_name = Utils.normalize_full_name(full_name)
			if not Utils.is_valid_full_name(normalized_full_name):
				return InvalidValueError(cls.ENTITY, DbUser.COLUMN_FULL_NAME)

			full_name = normalized_full_name
		
		return (
			phone,
			email,
			full_name,
		)

	@classmethod
	@BaseService.transaction
	def register(
		cls,
		cur: psycopg.Cursor,
		phone: str,
		email: str | None,
		full_name: str,
		password_hash: str,
		created_by: int | None
	) -> ServiceResult:
		"""
			Errors:
			- InvalidValueError
			- AlreadyExistsError
			- NotFoundError
			- UnhandledError
		"""

		if not Utils.is_valid_password_hash(password_hash):
			return ServiceResult(error=InvalidValueError(cls.ENTITY, DbUser.COLUMN_PASSWORD_HASH))
		
		normalized = cls._normalize_fields_or_catch(
			phone,
			email,
			full_name
		)

		if isinstance(normalized, InvalidValueError):
			return ServiceResult(error=normalized)
		
		norm_phone, norm_email, norm_full_name = normalized
		return ServiceResult(
			result=UsersRepository.create(
				cur=cur,
				phone=norm_phone,
				email=norm_email,
				full_name=norm_full_name,
				password_hash=password_hash,
				created_by=created_by
			)
		)
	
	@classmethod
	@BaseService.transaction
	def update(
		cls,
		cur: psycopg.Cursor,
		token: TokenPayload,
		phone: str | Unset = UNSET,
		email: str | None | Unset = UNSET,
		full_name: str | Unset = UNSET
	) -> ServiceResult:
		"""
			Errors:
			- InvalidValueError
			- AlreadyExistsError
			- NotFoundError
			- UnhandledError
		"""

		normalized = cls._normalize_fields_or_catch(
			phone,
			email,
			full_name
		)

		if isinstance(normalized, InvalidValueError):
			return ServiceResult(error=normalized)
		
		norm_phone, norm_email, norm_full_name = normalized
		updated = UsersRepository.update(
			cur=cur,
			user_id=token.user_id,
			token_ver=token.token_ver,
			phone=norm_phone,
			email=norm_email,
			full_name=norm_full_name
		)

		if not updated:
			return ServiceResult(error=InvalidValueError(cls.ENTITY, DbUser.COLUMN_TOKEN_VER))
		return ServiceResult()
		
	@classmethod
	@BaseService.transaction
	def set_password(
		cls,
		cur: psycopg.Cursor,
		token: TokenPayload,
		password_hash: str
	) -> ServiceResult:
		"""
			Errors:
			- InvalidValueError
			- NotFoundError
			- UnhandledError
		"""

		if not Utils.is_valid_password_hash(password_hash):
			return ServiceResult(error=InvalidValueError(cls.ENTITY, DbUser.COLUMN_PASSWORD_HASH))

		updated = UsersRepository.set_password(
			cur=cur,
			user_id=token.user_id,
			token_ver=token.token_ver,
			password_hash=password_hash
		)

		if updated is None:
			return ServiceResult(error=InvalidValueError(cls.ENTITY, DbUser.COLUMN_TOKEN_VER))
		return ServiceResult(result=updated)
			
	@classmethod
	@BaseService.transaction
	def block(
		cls,
		cur: psycopg.Cursor,
		user_id: int,
		blocked_by: int
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- UnhandledError
		"""

		user = UsersRepository.get_by_id(cur, user_id)
		if not user:
			return ServiceResult(error=NotFoundError(cls.ENTITY, DbUser.COLUMN_ID))
		
		UsersRepository.block(cur, user_id, blocked_by)
		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def unblock(
		cls,
		cur: psycopg.Cursor,
		user_id: int
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- UnhandledError
		"""

		user = UsersRepository.get_by_id(cur, user_id)
		if not user:
			return ServiceResult(error=NotFoundError(cls.ENTITY, DbUser.COLUMN_ID))
		
		UsersRepository.unblock(cur, user_id)
		return ServiceResult()
		
	@classmethod
	@BaseService.transaction
	def delete(
		cls,
		cur: psycopg.Cursor,
		user_id: int,
		deleted_by: int
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- UnhandledError
		"""

		user = UsersRepository.get_by_id(cur, user_id)
		if not user:
			return ServiceResult(error=NotFoundError(cls.ENTITY, DbUser.COLUMN_ID))
		
		UsersRepository.soft_delete(cur, user_id, deleted_by)
		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def restore(
		cls,
		cur: psycopg.Cursor,
		user_id: int
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- UnhandledError
		"""

		user = UsersRepository.get_by_id(cur, user_id)
		if not user:
			return ServiceResult(error=NotFoundError(cls.ENTITY, DbUser.COLUMN_ID))
		
		UsersRepository.restore(cur, user_id)
		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def get_by_id(
		cls,
		cur: psycopg.Cursor,
		user_id: int
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- UnhandledError
		"""

		user = UsersRepository.get_by_id(cur, user_id)
		if not user:
			return ServiceResult(error=NotFoundError(cls.ENTITY, DbUser.COLUMN_ID))
		return ServiceResult(result=user)

	@classmethod
	@BaseService.transaction
	def get_by_phone(
		cls,
		cur: psycopg.Cursor,
		phone: str
	) -> ServiceResult:
		"""
			Errors:
			- InvalidValueError
			- NotFoundError
			- UnhandledError
		"""

		norm_phone = Utils.normalize_phone(phone)
		if not Utils.is_valid_phone(norm_phone):
			return ServiceResult(error=InvalidValueError(cls.ENTITY, DbUser.COLUMN_PHONE))

		user = UsersRepository.get_by_phone(cur, norm_phone)
		if not user:
			return ServiceResult(error=NotFoundError(cls.ENTITY, DbUser.COLUMN_PHONE))
		return ServiceResult(result=user)


	@classmethod
	@BaseService.transaction
	def get_by_email(
		cls,
		cur: psycopg.Cursor,
		email: str
	) -> ServiceResult:
		"""
			Errors:
			- InvalidValueError
			- NotFoundError
			- UnhandledError
		"""

		norm_email = Utils.normalize_email(email)
		if not Utils.is_valid_email(norm_email):
			return ServiceResult(error=InvalidValueError(cls.ENTITY, DbUser.COLUMN_EMAIL))

		user = UsersRepository.get_by_email(cur, norm_email)
		if not user:
			return ServiceResult(error=NotFoundError(cls.ENTITY, DbUser.COLUMN_EMAIL))
		return ServiceResult(result=user)
	
	@classmethod
	@BaseService.transaction
	def search(
		cls,
		cur: psycopg.Cursor,
		search: str | None = None,
		exclude_deleted: bool = True,
		exclude_blocked: bool = True,
		limit: int = 50,
		offset: int = 0
	) -> ServiceResult:
		"""
			Errors:
			- UnhandledError
		"""

		return ServiceResult(
			result=UsersRepository.search(
				cur=cur,
				search=search,
				exclude_deleted=exclude_deleted,
				exclude_blocked=exclude_blocked,
				limit=limit,
				offset=offset
			)
		)
