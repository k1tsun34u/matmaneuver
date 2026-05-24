import psycopg
from app.utils import Utils
from app.unset import Unset, UNSET
from app.models.db.db_user import DbUser
from app.models.public.employee import Employee
from app.types.update_result import UpdateResult
from app.types.token_payload import TokenPayload
from app.services.base_service import BaseService
from app.types.service_result import ServiceResult
from app.types.permission_code import PermissionCode
from app.errors.not_found_error import NotFoundError
from app.errors.not_allowed_error import NotAllowedError
from app.types.transaction_helper import TransactionHelper
from app.errors.invalid_value_error import InvalidValueError
from app.repositories.public.users_repository import UsersRepository
from app.repositories.public.employee_permissions_repository import EmployeePermissionsRepository as EPR


class UsersService(BaseService):
	KEY_HELPERS = (TransactionHelper(DbUser.ENTITY, DbUser.TABLE, (
		DbUser.COLUMN_PHONE,
		DbUser.COLUMN_EMAIL,
	)),)

	FKEY_HELPERS = (TransactionHelper(DbUser.ENTITY, DbUser.TABLE, (
		DbUser.COLUMN_BLOCKED_BY,
		DbUser.COLUMN_DELETED_BY,
		DbUser.COLUMN_CREATED_BY,
	)),)

	@classmethod
	def _normalize_fields_or_catch(
		cls,
		phone: str | Unset,
		email: str | None | Unset,
		full_name: str | Unset
	) -> tuple[str | Unset, str | None | Unset, str | Unset] | InvalidValueError:
		if not isinstance(phone, Unset):
			normalized_phone = Utils.normalize_phone(phone)
			if not Utils.is_valid_phone(normalized_phone):
				return InvalidValueError(DbUser.ENTITY, DbUser.COLUMN_PHONE)
			
			phone = normalized_phone
		
		if not (isinstance(email, Unset) or email is None):
			normalized_email = Utils.normalize_email(email)
			if not Utils.is_valid_email(normalized_email):
				return InvalidValueError(DbUser.ENTITY, DbUser.COLUMN_EMAIL)
			
			email = normalized_email
		
		if not isinstance(full_name, Unset):
			normalized_full_name = Utils.normalize_full_name(full_name)
			if not Utils.is_valid_full_name(normalized_full_name):
				return InvalidValueError(DbUser.ENTITY, DbUser.COLUMN_FULL_NAME)

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
			- NotAllowedError
			- InvalidValueError
			- AlreadyExistsError
			- NotFoundError
			- UnhandledError
		"""

		if created_by is not None and not EPR.has_permission(cur, created_by, PermissionCode.CREATE_USER):
			return ServiceResult(error=NotAllowedError(PermissionCode.CREATE_USER, DbUser.COLUMN_CREATED_BY))

		if not Utils.is_valid_password_hash(password_hash):
			return ServiceResult(error=InvalidValueError(DbUser.ENTITY, DbUser.COLUMN_PASSWORD_HASH))
		
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
			- NotFoundError
			- AlreadyExistsError
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
		tmp = UsersRepository.update(
			cur=cur,
			user_id=token.user_id,
			token_ver=token.token_ver,
			norm_phone=norm_phone,
			norm_email=norm_email,
			norm_full_name=norm_full_name
		)

		match tmp:
			case UpdateResult.FAIL_CONDITION:
				return ServiceResult(error=InvalidValueError(DbUser.ENTITY, DbUser.COLUMN_TOKEN_VER))
			case UpdateResult.FAIL_NOT_FOUND:
				return ServiceResult(error=NotFoundError(DbUser.ENTITY, DbUser.COLUMN_ID))
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
			return ServiceResult(error=InvalidValueError(DbUser.ENTITY, DbUser.COLUMN_PASSWORD_HASH))

		tmp = UsersRepository.set_password(
			cur=cur,
			user_id=token.user_id,
			token_ver=token.token_ver,
			password_hash=password_hash
		)

		match tmp[0]:
			case UpdateResult.FAIL_CONDITION:
				return ServiceResult(error=InvalidValueError(DbUser.ENTITY, DbUser.COLUMN_TOKEN_VER))
			case UpdateResult.FAIL_NOT_FOUND:
				return ServiceResult(error=NotFoundError(DbUser.ENTITY, DbUser.COLUMN_ID))
		return ServiceResult(result=tmp[1])
			
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
			- NotAllowedError
			- NotFoundError
			- UnhandledError
		"""

		if not EPR.has_permission(cur, blocked_by, PermissionCode.BLOCK_USER):
			return ServiceResult(error=NotAllowedError(PermissionCode.BLOCK_USER, DbUser.COLUMN_BLOCKED_BY))
		
		if UsersRepository.block(cur, user_id, blocked_by) == UpdateResult.FAIL_NOT_FOUND:
			return ServiceResult(error=NotFoundError(DbUser.ENTITY, DbUser.COLUMN_ID))
		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def unblock(
		cls,
		cur: psycopg.Cursor,
		user_id: int,
		unblocked_by: int
	) -> ServiceResult:
		"""
			Errors:
			- NotAllowedError
			- NotFoundError
			- UnhandledError
		"""

		if not EPR.has_permission(cur, unblocked_by, PermissionCode.UNBLOCK_USER):
			return ServiceResult(error=NotAllowedError(PermissionCode.UNBLOCK_USER))
		
		if UsersRepository.unblock(cur, user_id) == UpdateResult.FAIL_NOT_FOUND:
			return ServiceResult(error=NotFoundError(DbUser.ENTITY, DbUser.COLUMN_ID))
		return ServiceResult()
		
	@classmethod
	@BaseService.transaction
	def soft_delete(
		cls,
		cur: psycopg.Cursor,
		user_id: int,
		deleted_by: int | None
	) -> ServiceResult:
		"""
			Errors:
			- NotAllowedError
			- NotFoundError
			- UnhandledError
		"""

		if deleted_by is not None and not EPR.has_permission(cur, deleted_by, PermissionCode.DELETE_USER):
			return ServiceResult(error=NotAllowedError(PermissionCode.DELETE_USER, DbUser.COLUMN_DELETED_BY))
		
		if UsersRepository.soft_delete(cur, user_id, deleted_by) == UpdateResult.FAIL_NOT_FOUND:
			return ServiceResult(error=NotFoundError(DbUser.ENTITY, DbUser.COLUMN_ID))
		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def restore(
		cls,
		cur: psycopg.Cursor,
		user_id: int,
		restored_by: int | None
	) -> ServiceResult:
		"""
			Errors:
			- NotAllowedError
			- NotFoundError
			- UnhandledError
		"""

		if restored_by is not None and not EPR.has_permission(cur, restored_by, PermissionCode.CREATE_USER):
			return ServiceResult(error=NotAllowedError(PermissionCode.CREATE_USER))
		
		if UsersRepository.restore(cur, user_id) == UpdateResult.FAIL_NOT_FOUND:
			return ServiceResult(error=NotFoundError(DbUser.ENTITY, DbUser.COLUMN_ID))
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
			return ServiceResult(error=NotFoundError(DbUser.ENTITY, DbUser.COLUMN_ID))
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
			return ServiceResult(error=InvalidValueError(DbUser.ENTITY, DbUser.COLUMN_PHONE))

		user = UsersRepository.get_by_phone(cur, norm_phone)
		if not user:
			return ServiceResult(error=NotFoundError(DbUser.ENTITY, DbUser.COLUMN_PHONE))
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
			return ServiceResult(error=InvalidValueError(DbUser.ENTITY, DbUser.COLUMN_EMAIL))

		user = UsersRepository.get_by_email(cur, norm_email)
		if not user:
			return ServiceResult(error=NotFoundError(DbUser.ENTITY, DbUser.COLUMN_EMAIL))
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
