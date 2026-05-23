import psycopg
from app.utils import Utils
from app.models.public.role import Role
from app.services.base_service import BaseService
from app.types.service_result import ServiceResult
from app.errors.not_found_error import NotFoundError
from app.errors.not_allowed_error import NotAllowedError
from app.types.deactivate_result import DeactivateResult
from app.types.transaction_helper import TransactionHelper
from app.errors.invalid_value_error import InvalidValueError
from app.repositories.public.roles_repository import RolesRepository


class RolesService(BaseService):
	ENTITY = "Role"
	KEY_HELPERS = (TransactionHelper(ENTITY, "roles", (Role.COLUMN_CODE,)),)
	FKEY_HELPERS = (TransactionHelper(ENTITY, "roles", (
		Role.COLUMN_DEACTIVATED_BY,
		Role.COLUMN_CREATED_BY,
	)),)

	@classmethod
	@BaseService.transaction
	def create(
		cls,
		cur: psycopg.Cursor,
		code: str,
		is_system: bool,
		created_by: int | None
	) -> ServiceResult:
		"""
			Errors:
			- InvalidValueError
			- AlreadyExistsError
			- NotFoundError
			- UnhandledError
		"""

		norm_code = Utils.normalize_code(code)
		if not Utils.is_valid_code(norm_code):
			return ServiceResult(error=InvalidValueError(cls.ENTITY, Role.COLUMN_CODE))
		
		return ServiceResult(result=RolesRepository.create(
				cur=cur,
				code=norm_code,
				is_system=is_system,
				created_by=created_by
			)
		)
	
	@classmethod
	@BaseService.transaction
	def deactivate(
		cls,
		cur: psycopg.Cursor,
		role_id: int,
		deactivated_by: int
	) -> ServiceResult:
		"""
			Errors:
			- NotAllowedError
			- InvalidValueError
			- NotFoundError
			- UnhandledError
		"""

		tmp = RolesRepository.deactivate(cur, role_id, deactivated_by)
		if tmp == DeactivateResult.FAIL_IS_SYSTEM:
			return ServiceResult(error=NotAllowedError(cls.ENTITY, Role.COLUMN_IS_SYSTEM))
		elif tmp == DeactivateResult.FAIL_NOT_FOUND:
			return ServiceResult(error=NotFoundError(cls.ENTITY, Role.COLUMN_ID))
		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def restore(
		cls,
		cur: psycopg.Cursor,
		role_id: int
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- UnhandledError
		"""

		role = RolesRepository.get_by_id(cur, role_id)
		if not role:
			return ServiceResult(error=NotFoundError(cls.ENTITY, Role.COLUMN_ID))

		RolesRepository.restore(cur, role_id)
		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def get_by_id(
		cls,
		cur: psycopg.Cursor,
		role_id: int
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- UnhandledError
		"""

		role = RolesRepository.get_by_id(cur, role_id)
		if not role:
			return ServiceResult(error=NotFoundError(cls.ENTITY, Role.COLUMN_ID))
		return ServiceResult(result=role)
	
	@classmethod
	@BaseService.transaction
	def get_by_code(
		cls,
		cur: psycopg.Cursor,
		code: str
	) -> ServiceResult:
		"""
			Errors:
			- InvalidValueError
			- NotFoundError
			- UnhandledError
		"""

		norm_code = Utils.normalize_code(code)
		if not Utils.is_valid_code(norm_code):
			return ServiceResult(error=InvalidValueError(cls.ENTITY, Role.COLUMN_CODE))

		role = RolesRepository.get_by_code(cur, norm_code)
		if not role:
			return ServiceResult(error=NotFoundError(cls.ENTITY, Role.COLUMN_CODE))
		return ServiceResult(result=role)
	
	@classmethod
	@BaseService.transaction
	def search(
		cls,
		cur: psycopg.Cursor,
		search: str | None = None,
		exclude_deactivated: bool = True,
		limit: int = 50,
		offset: int = 0
	) -> ServiceResult:
		"""
			Errors:
			- UnhandledError
		"""

		return ServiceResult(
			result=RolesRepository.search(
				cur=cur,
				search=search,
				exclude_deactivated=exclude_deactivated,
				limit=limit,
				offset=offset
			)
		)
