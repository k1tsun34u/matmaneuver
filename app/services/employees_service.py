import psycopg
from datetime import date
from app.models.public.employee import Employee
from app.services.base_service import BaseService
from app.types.service_result import ServiceResult
from app.models.public.permission import Permission
from app.errors.not_found_error import NotFoundError
from app.errors.not_allowed_error import NotAllowedError
from app.types.transaction_helper import TransactionHelper
from app.errors.invalid_value_error import InvalidValueError
from app.repositories.public.employees_repository import EmployeesRepository
from app.repositories.public.employee_roles_repository import EmployeeRolesRepository
from app.repositories.public.employee_permissions_repository import EmployeePermissionsRepository


class EmployeesService(BaseService):
	ENTITY = "Employee"
	KEY_HELPERS = (TransactionHelper(ENTITY, "employees", tuple()),)
	FKEY_HELPERS = (TransactionHelper(ENTITY, "employees", (
		Employee.COLUMN_USER_ID,
		Employee.COLUMN_HIRED_BY,
		Employee.COLUMN_FIRED_BY,
		Employee.COLUMN_CREATED_BY,
	)),)

	@classmethod
	def _has_permission(
		cls,
		cur: psycopg.Cursor,
		employee_id: int,
		permission_code: str
	) -> bool:
		return EmployeePermissionsRepository.has_permission(
			cur,
			employee_id,
			permission_code
		)

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

		if hired_by and not cls._has_permission(cur, hired_by, Permission.HIRE_EMPLOYEE):
			return NotAllowedError(cls.ENTITY, Employee.COLUMN_HIRED_BY)

		if created_by and not cls._has_permission(cur, created_by, Permission.CREATE_EMPLOYEE):
			return NotAllowedError(cls.ENTITY, Employee.COLUMN_CREATED_BY)
			
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

		if not cls._has_permission(cur, fired_by, Permission.FIRE_EMPLOYEE):
			return NotAllowedError(cls.ENTITY, Employee.COLUMN_FIRED_BY)

		employee = EmployeesRepository.get_by_id(cur, employee_id)
		if not employee:
			return ServiceResult(error=NotFoundError(cls.ENTITY, Employee.COLUMN_ID))
		
		EmployeesRepository.fire(cur, employee_id, fired_by)
		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def rehire(
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
		
		EmployeesRepository.rehire(cur, employee_id)
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
			return ServiceResult(error=NotFoundError(cls.ENTITY, Employee.COLUMN_ID))
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
		return ServiceResult(result=EmployeePermissionsRepository.get_permissions(cur, employee_id))
