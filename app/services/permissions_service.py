import psycopg
from app.utils import Utils
from app.services.base_service import BaseService
from app.types.service_result import ServiceResult
from app.models.public.permission import Permission
from app.types.permission_code import PermissionCode
from app.errors.not_found_error import NotFoundError
from app.errors.not_allowed_error import NotAllowedError
from app.types.deactivate_result import DeactivateResult
from app.types.transaction_helper import TransactionHelper
from app.errors.invalid_value_error import InvalidValueError
from app.repositories.public.permissions_repository import PermissionsRepository
from app.repositories.public.employee_permissions_repository import EmployeePermissionsRepository as EPR


class PermissionsService(BaseService):
	ENTITY = "Permission"
	KEY_HELPERS = (TransactionHelper(ENTITY, "permissions", (Permission.COLUMN_CODE,)),)
	FKEY_HELPERS = (TransactionHelper(ENTITY, "permissions", (
		Permission.COLUMN_DEACTIVATED_BY,
		Permission.COLUMN_CREATED_BY,
	)),)

	@classmethod
	@BaseService.transaction
	def create(
		cls,
		cur: psycopg.Cursor,
		code: str,
		description: str | None,
		is_system: bool,
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

		if created_by is not None and not EPR.has_permission(cur, created_by, PermissionCode.CREATE_PERMISSION):
			return ServiceResult(error=NotAllowedError(PermissionCode.CREATE_PERMISSION, Permission.COLUMN_CREATED_BY))

		norm_code = Utils.normalize_code(code)
		if not Utils.is_valid_code(norm_code):
			return ServiceResult(error=InvalidValueError(cls.ENTITY, Permission.COLUMN_CODE))
		
		return ServiceResult(result=PermissionsRepository.create(
				cur=cur,
				code=norm_code,
				description=description,
				is_system=is_system,
				created_by=created_by
			)
		)
	
	@classmethod
	@BaseService.transaction
	def set_description(
		cls,
		cur: psycopg.Cursor,
		permission_id: int,
		description: str | None,
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- UnhandledError
		"""

		updated = PermissionsRepository.set_description(cur, permission_id, description)
		if not updated:
			return ServiceResult(error=NotFoundError(cls.ENTITY, Permission.COLUMN_ID))
		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def deactivate(
		cls,
		cur: psycopg.Cursor,
		permission_id: int,
		deactivated_by: int
	) -> ServiceResult:
		"""
			Errors:
			- NotAllowedError
			- InvalidValueError
			- NotFoundError
			- UnhandledError
		"""

		if not EPR.has_permission(cur, deactivated_by, PermissionCode.DEACTIVATE_PERMISSION):
			return ServiceResult(error=NotAllowedError(PermissionCode.DEACTIVATE_PERMISSION, Permission.COLUMN_DEACTIVATED_BY))

		tmp = PermissionsRepository.deactivate(cur, permission_id, deactivated_by)
		if tmp == DeactivateResult.FAIL_IS_SYSTEM:
			return ServiceResult(error=NotAllowedError(cls.ENTITY, Permission.COLUMN_IS_SYSTEM))
		elif tmp == DeactivateResult.FAIL_NOT_FOUND:
			return ServiceResult(error=NotFoundError(cls.ENTITY, Permission.COLUMN_ID))
		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def restore(
		cls,
		cur: psycopg.Cursor,
		permission_id: int,
		restored_by: int
	) -> ServiceResult:
		"""
			Errors:
			- NotAllowedError
			- NotFoundError
			- UnhandledError
		"""

		if not EPR.has_permission(cur, restored_by, PermissionCode.CREATE_PERMISSION):
			return ServiceResult(error=NotAllowedError(PermissionCode.CREATE_PERMISSION))

		permission = PermissionsRepository.get_by_id(cur, permission_id)
		if not permission:
			return ServiceResult(error=NotFoundError(cls.ENTITY, Permission.COLUMN_ID))

		if not PermissionsRepository.restore(cur, permission_id):
			return ServiceResult(error=NotFoundError(cls.ENTITY, Permission.COLUMN_ID))
		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def get_by_id(
		cls,
		cur: psycopg.Cursor,
		permission_id: int
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- UnhandledError
		"""

		permission = PermissionsRepository.get_by_id(cur, permission_id)
		if not permission:
			return ServiceResult(error=NotFoundError(cls.ENTITY, Permission.COLUMN_ID))
		return ServiceResult(result=permission)
	
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
			return ServiceResult(error=InvalidValueError(cls.ENTITY, Permission.COLUMN_CODE))

		permission = PermissionsRepository.get_by_code(cur, norm_code)
		if not permission:
			return ServiceResult(error=NotFoundError(cls.ENTITY, Permission.COLUMN_CODE))
		return ServiceResult(result=permission)
	
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
			result=PermissionsRepository.search(
				cur=cur,
				search=search,
				exclude_deactivated=exclude_deactivated,
				limit=limit,
				offset=offset
			)
		)
