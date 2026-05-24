import psycopg
from app.utils import Utils
from collections.abc import Sequence
from app.models.public.role import Role
from app.types.update_result import UpdateResult
from app.services.base_service import BaseService
from app.types.service_result import ServiceResult
from app.errors.not_found_error import NotFoundError
from app.types.permission_code import PermissionCode
from app.errors.not_allowed_error import NotAllowedError
from app.types.deactivate_result import DeactivateResult
from app.types.transaction_helper import TransactionHelper
from app.errors.invalid_value_error import InvalidValueError
from app.models.public.role_permission import RolePermission
from app.repositories.public.roles_repository import RolesRepository
from app.repositories.public.role_permissions_repository import RolePermissionsRepository as RPR
from app.repositories.public.employee_permissions_repository import EmployeePermissionsRepository as EPR


class RolesService(BaseService):
	KEY_HELPERS = (TransactionHelper(Role.ENTITY, Role.TABLE, (Role.COLUMN_CODE,)),)
	FKEY_HELPERS = (TransactionHelper(Role.ENTITY, Role.TABLE, (
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
			- NotAllowedError
			- AlreadyExistsError
			- NotFoundError
			- UnhandledError
		"""

		norm_code = Utils.normalize_code(code)
		if not Utils.is_valid_code(norm_code):
			return ServiceResult(error=InvalidValueError(Role.ENTITY, Role.COLUMN_CODE))
		
		if created_by is not None and not EPR.has_permission(cur, created_by, PermissionCode.CREATE_ROLE):
			return ServiceResult(error=NotAllowedError(PermissionCode.CREATE_ROLE, Role.COLUMN_CREATED_BY))
		
		return ServiceResult(
			result=RolesRepository.create(
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
		
		if not EPR.has_permission(cur, deactivated_by, PermissionCode.DEACTIVATE_ROLE):
			return ServiceResult(error=NotAllowedError(PermissionCode.DEACTIVATE_ROLE, Role.COLUMN_DEACTIVATED_BY))

		match RolesRepository.deactivate(cur, role_id, deactivated_by):
			case DeactivateResult.FAIL_IS_SYSTEM:
				return ServiceResult(error=NotAllowedError(Role.ENTITY, Role.COLUMN_IS_SYSTEM))
			case DeactivateResult.FAIL_NOT_FOUND:
				return ServiceResult(error=NotFoundError(Role.ENTITY, Role.COLUMN_ID))
		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def restore(
		cls,
		cur: psycopg.Cursor,
		role_id: int,
		restored_by: int | None
	) -> ServiceResult:
		"""
			Errors:
			- NotAllowedError
			- NotFoundError
			- UnhandledError
		"""
		
		if restored_by is not None and not EPR.has_permission(cur, restored_by, PermissionCode.CREATE_ROLE):
			return ServiceResult(error=NotAllowedError(PermissionCode.CREATE_ROLE))

		if RolesRepository.restore(cur, role_id) == UpdateResult.FAIL_NOT_FOUND:
				return ServiceResult(error=NotFoundError(Role.ENTITY, Role.COLUMN_ID))
		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def assign_permissions(
		cls,
		cur: psycopg.Cursor,
		role_id: int,
		permission_ids: Sequence[int],
		assigned_by: int | None
	) -> ServiceResult:
		"""
			Errors:
			- NotAllowedError
			- NotFoundError
			- UnhandledError
		"""

		if assigned_by is not None and not EPR.has_permission(cur, assigned_by, PermissionCode.ASSIGN_PERMISSION):
			return ServiceResult(error=NotAllowedError(PermissionCode.ASSIGN_PERMISSION, RolePermission.COLUMN_ASSIGNED_BY))
		
		RPR.assign_many(cur, role_id, permission_ids, assigned_by)
		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def unassign_permissions(
		cls,
		cur: psycopg.Cursor,
		role_id: int,
		permission_ids: Sequence[int],
		unassigned_by: int | None
	) -> ServiceResult:
		"""
			Errors:
			- NotAllowedError
			- NotFoundError
			- UnhandledError
		"""

		if unassigned_by is not None and not EPR.has_permission(cur, unassigned_by, PermissionCode.UNASSIGN_PERMISSION):
			return ServiceResult(error=NotAllowedError(PermissionCode.UNASSIGN_PERMISSION))
		
		RPR.unassign_many(cur, role_id, permission_ids)
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
			return ServiceResult(error=NotFoundError(Role.ENTITY, Role.COLUMN_ID))
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
			return ServiceResult(error=InvalidValueError(Role.ENTITY, Role.COLUMN_CODE))

		role = RolesRepository.get_by_code(cur, norm_code)
		if not role:
			return ServiceResult(error=NotFoundError(Role.ENTITY, Role.COLUMN_CODE))
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
