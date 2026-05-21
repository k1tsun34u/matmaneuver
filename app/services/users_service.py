
from app.db import Db
from app.utils import Utils
import psycopg.errors as errors
from app.unset import Unset, UNSET
from app.models.db.db_user import DbUser
from app.errors.other import InternalError
from app.repositories.public.users_repository import UsersRepository
from app.errors.validation import (
	InvalidPhoneError,
	InvalidEmailError,
	InvalidFullNameError,
	InvalidPasswordHashError
)
from app.errors.user import (
	UserPhoneAlreadyExistsError,
	UserEmailAlreadyExistsError,
	UserNotFoundError,

	EmployeeNotFoundError
)


class UsersService:
	MAX_PHONE_LENGTH = 32
	MAX_EMAIL_LENGTH = 256

	@classmethod
	def _normalize_fields_or_raise(
		cls,
		phone: str | Unset,
		email: str | None | Unset,
		full_name: str | Unset
	) -> tuple[str | Unset, str | None | Unset, str | Unset]:
		if not isinstance(phone, Unset):
			normalized_phone = Utils.normalize_phone(phone)
			is_valid_phone = (
				len(normalized_phone) <= cls.MAX_PHONE_LENGTH
				and Utils.is_valid_phone(normalized_phone)
			)

			if not is_valid_phone:
				raise InvalidPhoneError(phone)
			
			phone = normalized_phone
		
		if not (isinstance(email, Unset) or email is None):
			normalized_email = Utils.normalize_email(email)
			is_valid_email = (
				len(normalized_email) <= cls.MAX_EMAIL_LENGTH
				and Utils.is_valid_email(normalized_email)
			)

			if not is_valid_email:
				raise InvalidEmailError(email)
			
			email = normalized_email
		
		if not isinstance(full_name, Unset):
			normalized_full_name = Utils.normalize_full_name(full_name)
			if not Utils.is_valid_full_name(normalized_full_name):
				raise InvalidFullNameError(full_name)

			full_name = normalized_full_name
		
		return (
			phone,
			email,
			full_name,
		)
	
	@staticmethod
	def _require_user(cur, user_id: int) -> DbUser:
		user = UsersRepository.get_by_id(cur, user_id)
		if user is None:
			raise UserNotFoundError(user_id)
		return user

	@classmethod
	def register_user(
		cls,
		phone: str,
		email: str | None,
		full_name: str,
		password_hash: str,
		created_by: int | None
	) -> int:
		"""
			Returns user id or raises:
			- InvalidPhoneError
			- InvalidEmailError
			- UserPhoneAlreadyExistsError
			- UserEmailAlreadyExistsError
			- InternalError
		"""

		norm_phone, norm_email, norm_full_name = cls._normalize_fields_or_raise(
			phone,
			email,
			full_name
		)

		if not password_hash:
			raise InvalidPasswordHashError(password_hash)

		try:
			with Db.connection() as conn:
				with conn.cursor() as cur:
					return UsersRepository.create(
						cur=cur,
						phone=norm_phone,
						email=norm_email,
						full_name=norm_full_name,
						password_hash=password_hash,
						created_by=created_by
					)
		except errors.UniqueViolation as e:
			constraint = e.diag.constraint_name
			if constraint == "users_phone_key":
				raise UserPhoneAlreadyExistsError(phone)
			elif constraint == "users_email_key":
				raise UserEmailAlreadyExistsError(email)
			raise
		except errors.ForeignKeyViolation as e:
			constraint = e.diag.constraint_name
			if constraint == "users_created_by_fkey":
				raise EmployeeNotFoundError(created_by)
			raise
		except errors.Error as e:
			raise InternalError() from e
	
	@classmethod
	def update_user(
		cls,
		user_id: int,
		phone: str | Unset = UNSET,
		email: str | None | Unset = UNSET,
		full_name: str | Unset = UNSET,
		password_hash: str | Unset = UNSET
	) -> None:
		"""
			Updates `phone`/`email`/`full_name`/`password_hash` or raises:
			- UserNotFoundError
			- UserPhoneAlreadyExistsError
			- UserEmailAlreadyExistsError
			- InternalError
		"""

		norm_phone, norm_email, norm_full_name = cls._normalize_fields_or_raise(
			phone,
			email,
			full_name
		)

		if not isinstance(password_hash, Unset) and not password_hash:
			raise InvalidPasswordHashError(password_hash)

		try:
			with Db.connection() as conn:
				with conn.cursor() as cur:
					UsersRepository.update(
						cur=cur,
						user_id=user_id,
						phone=norm_phone,
						email=norm_email,
						full_name=norm_full_name,
						password_hash=password_hash
					)
		except errors.UniqueViolation as e:
			constraint = e.diag.constraint_name
			if constraint == "users_phone_key":
				raise UserPhoneAlreadyExistsError(phone)
			elif constraint == "users_email_key":
				raise UserEmailAlreadyExistsError(email)
			raise
		except errors.Error as e:
			raise InternalError() from e
				
	@classmethod
	def block_user(cls, user_id: int, blocked_by: int) -> None:
		"""
			Blocks user or raises:
			- UserNotFoundError
			- EmployeeNotFoundError
			- InternalError
		"""

		try:
			with Db.connection() as conn:
				with conn.cursor() as cur:
					if not UsersRepository.block(cur, user_id, blocked_by):
						raise UserNotFoundError(user_id)
		except errors.ForeignKeyViolation as e:
			constraint = e.diag.constraint_name
			if constraint == "users_blocked_by_fkey":
				raise EmployeeNotFoundError(blocked_by)
			raise
		except errors.Error as e:
			raise InternalError() from e
	
	@classmethod
	def unblock_user(cls, user_id: int) -> None:
		"""
			Unblocks user or raises:
			- UserNotFoundError
			- InternalError
		"""

		try:
			with Db.connection() as conn:
				with conn.cursor() as cur:
					if not UsersRepository.unblock(cur, user_id):
						raise UserNotFoundError(user_id)
		except errors.Error as e:
			raise InternalError() from e
		
	@classmethod
	def delete_user(cls, user_id: int, deleted_by: int) -> None:
		"""
			Deletes(soft delete) user or raises:
			- UserNotFoundError
			- EmployeeNotFoundError
			- InternalError
		"""

		try:
			with Db.connection() as conn:
				with conn.cursor() as cur:
					if not UsersRepository.soft_delete(cur, user_id, deleted_by):
						raise UserNotFoundError(user_id)
		except errors.ForeignKeyViolation as e:
			constraint = e.diag.constraint_name
			if constraint == "users_deleted_by_fkey":
				raise EmployeeNotFoundError(deleted_by)
			raise
		except errors.Error as e:
			raise InternalError() from e
	
	@classmethod
	def restore_user(cls, user_id: int) -> None:
		"""
			Restores user or raises:
			- UserNotFoundError
			- InternalError
		"""

		try:
			with Db.connection() as conn:
				with conn.cursor() as cur:
					if not UsersRepository.restore(cur, user_id):
						raise UserNotFoundError(user_id)
		except errors.Error as e:
			raise InternalError() from e
	
	@classmethod
	def is_user_blocked(cls, user_id: int) -> bool:
		"""
			Returns True or False
			depending on whether the user is blocked
			or raises:
			- UserNotFoundError
			- InternalError
		"""

		try:
			with Db.connection() as conn:
				with conn.cursor() as cur:
					user = cls._require_user(cur, user_id)
					return user.blocked_at is not None
		except errors.Error as e:
			raise InternalError() from e
	
	@classmethod
	def is_user_deleted(cls, user_id: int) -> bool:
		"""
			Returns True or False
			depending on whether the user is deleted
			or raises:
			- UserNotFoundError
			- InternalError
		"""

		try:
			with Db.connection() as conn:
				with conn.cursor() as cur:
					user = cls._require_user(cur, user_id)
					return user.deleted_at is not None
		except errors.Error as e:
			raise InternalError() from e
	
	@classmethod
	def get_user_by_id(cls, user_id: int) -> DbUser:
		"""
			Returns user or raises:
			- UserNotFoundError
			- InternalError
		"""

		try:
			with Db.connection() as conn:
				with conn.cursor() as cur:
					return cls._require_user(cur, user_id)
		except errors.Error as e:
			raise InternalError() from e
