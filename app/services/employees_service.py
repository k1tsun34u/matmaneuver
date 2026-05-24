import psycopg
from datetime import date
from collections.abc import Sequence
from app.models.public.employee import Employee
from app.types.update_result import UpdateResult
from app.services.base_service import BaseService
from app.types.service_result import ServiceResult
from app.types.permission_code import PermissionCode
from app.errors.not_found_error import NotFoundError
from app.errors.not_allowed_error import NotAllowedError
from app.models.public.employee_role import EmployeeRole
from app.types.transaction_helper import TransactionHelper
from app.errors.invalid_value_error import InvalidValueError
from app.repositories.public.employees_repository import EmployeesRepository
from app.repositories.public.employee_roles_repository import EmployeeRolesRepository
from app.repositories.public.employee_permissions_repository import EmployeePermissionsRepository as EPR


class EmployeesService(BaseService):
	ENTITY = "Employee"
	KEY_HELPERS = (TransactionHelper(ENTITY, "employees", (Employee.COLUMN_USER_ID,)),)
	FKEY_HELPERS = (TransactionHelper(ENTITY, "employees", (
		Employee.COLUMN_USER_ID,
		Employee.COLUMN_HIRED_BY,
		Employee.COLUMN_FIRED_BY,
		Employee.COLUMN_CREATED_BY,
	)),)

	@classmethod
	@BaseService.transaction
	def register(
		cls,
		cur: psycopg.Cursor,
		user_id: int,
		hired_by: int | None,
		hired_at: date,
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

		if hired_by is not None and not EPR.has_permission(cur, hired_by, PermissionCode.HIRE_EMPLOYEE):
			return ServiceResult(error=NotAllowedError(PermissionCode.HIRE_EMPLOYEE, Employee.COLUMN_HIRED_BY))

		if created_by is not None and not EPR.has_permission(cur, created_by, PermissionCode.CREATE_EMPLOYEE):
			return ServiceResult(error=NotAllowedError(PermissionCode.CREATE_EMPLOYEE, Employee.COLUMN_CREATED_BY))
			
		if hired_at > date.today():
			return ServiceResult(error=InvalidValueError(cls.ENTITY, Employee.COLUMN_HIRED_AT))
		
		return ServiceResult(
			result=EmployeesRepository.create(
				cur=cur,
				user_id=user_id,
				hired_by=hired_by,
				hired_at=hired_at,
				created_by=created_by
			)
		)
	
	@classmethod
	@BaseService.transaction
	def fire(
		cls,
		cur: psycopg.Cursor,
		employee_id: int,
		fired_by: int
	) -> ServiceResult:
		"""
			Errors:
			- NotAllowedError
			- NotFoundError
			- UnhandledError
		"""

		if not EPR.has_permission(cur, fired_by, PermissionCode.FIRE_EMPLOYEE):
			return ServiceResult(error=NotAllowedError(PermissionCode.FIRE_EMPLOYEE, Employee.COLUMN_FIRED_BY))
		
		if EmployeesRepository.fire(cur, employee_id, fired_by) == UpdateResult.FAIL_NOT_FOUND:
			return ServiceResult(error=NotFoundError(cls.ENTITY, Employee.COLUMN_ID))
		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def rehire(
		cls,
		cur: psycopg.Cursor,
		employee_id: int,
		hired_by: int
	) -> ServiceResult:
		"""
			Errors:
			- NotAllowedError
			- NotFoundError
			- UnhandledError
		"""

		if not EPR.has_permission(cur, hired_by, PermissionCode.HIRE_EMPLOYEE):
			return ServiceResult(error=NotAllowedError(PermissionCode.HIRE_EMPLOYEE, Employee.COLUMN_HIRED_BY))
		
		updated = EmployeesRepository.rehire(cur, employee_id, hired_by)
		if updated == UpdateResult.FAIL_NOT_FOUND:
			return ServiceResult(error=NotFoundError(cls.ENTITY, Employee.COLUMN_ID))
		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def assign_roles(
		cls,
		cur: psycopg.Cursor,
		employee_id: int,
		role_ids: Sequence[int],
		assigned_by: int | None
	) -> ServiceResult:
		"""
			Errors:
			- NotAllowedError
			- NotFoundError
			- UnhandledError
		"""
		
		if assigned_by is not None and not EPR.has_permission(cur, assigned_by, PermissionCode.ASSIGN_ROLE):
			return ServiceResult(error=NotAllowedError(PermissionCode.ASSIGN_ROLE, EmployeeRole.COLUMN_ASSIGNED_BY))

		EmployeeRolesRepository.assign_many(
			cur=cur,
			employee_id=employee_id,
			role_ids=role_ids,
			assigned_by=assigned_by
		)

		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def unassign_roles(
		cls,
		cur: psycopg.Cursor,
		employee_id: int,
		role_ids: Sequence[int],
		unassigned_by: int | None
	) -> ServiceResult:
		"""
			Errors:
			- NotAllowedError
			- NotFoundError
			- UnhandledError
		"""
		
		if unassigned_by is not None and not EPR.has_permission(cur, unassigned_by, PermissionCode.UNASSIGN_ROLE):
			return ServiceResult(error=NotAllowedError(PermissionCode.UNASSIGN_ROLE, EmployeeRole.COLUMN_ASSIGNED_BY))

		EmployeeRolesRepository.unassign_many(
			cur=cur,
			employee_id=employee_id,
			role_ids=role_ids
		)

		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def get_by_id(
		cls,
		cur: psycopg.Cursor,
		employee_id: int
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- UnhandledError
		"""

		employee = EmployeesRepository.get_by_id(cur, employee_id)
		if not employee:
			return ServiceResult(error=NotFoundError(cls.ENTITY, Employee.COLUMN_ID))
		return ServiceResult(result=employee)
	
	@classmethod
	@BaseService.transaction
	def get_by_user_id(
		cls,
		cur: psycopg.Cursor,
		user_id: int
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- UnhandledError
		"""

		employee = EmployeesRepository.get_by_user_id(cur, user_id)
		if not employee:
			return ServiceResult(error=NotFoundError(cls.ENTITY, Employee.COLUMN_USER_ID))
		return ServiceResult(result=employee)
	
	@classmethod
	@BaseService.transaction
	def get_roles(
		cls,
		cur: psycopg.Cursor,
		employee_id: int
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- UnhandledError
		"""
		
		employee = EmployeesRepository.get_by_id(cur, employee_id)
		if not employee:
			return ServiceResult(error=NotFoundError(cls.ENTITY, Employee.COLUMN_ID))
		return ServiceResult(result=EmployeeRolesRepository.get_roles(cur, employee_id))

	@classmethod
	@BaseService.transaction
	def get_permissions(
		cls,
		cur: psycopg.Cursor,
		employee_id: int
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- UnhandledError
		"""
		
		employee = EmployeesRepository.get_by_id(cur, employee_id)
		if not employee:
			return ServiceResult(error=NotFoundError(cls.ENTITY, Employee.COLUMN_ID))
		return ServiceResult(result=EPR.get_permissions(cur, employee_id))
