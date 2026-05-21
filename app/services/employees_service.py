from app.db import Db
from datetime import date
from app.models.public.role import Role
from app.errors.other import InternalError
from app.services.users_service import UsersService
from app.repositories.public.users_repository import UsersRepository
from app.repositories.public.roles_repository import RolesRepository
from app.repositories.public.employees_repository import EmployeesRepository
from app.repositories.public.employee_roles_repository import EmployeeRolesRepository
from app.errors.user import (
	UserPhoneAlreadyExistsError,
	UserEmailAlreadyExistsError,

	EmployeeNotFoundError,
	EmployeeNotFoundByUserError,

	RoleNotFoundError
)


class EmployeesService:
	@staticmethod
	def register_employee(
		phone: str,
		email: str | None,
		full_name: str,
		password_hash: str,
		hired_by: int | None,
		hired_at: date,
		created_by: int | None
	) -> tuple[int, int]:
		pass
	
	@staticmethod
	def fire_employee(employee_id: int, fired_by: int):
		pass
	
	@staticmethod
	def rehire_employee(employee_id: int):
		pass

	@staticmethod
	def get_employee_by_user_id(user_id: int) -> int:
		pass
	
	@staticmethod
	def assign_employee_roles(
		employee_id: int,
		role_ids: list[int],
		assigned_by: int | None
	):
		pass
	
	@staticmethod
	def unassign_employee_roles(
		employee_id: int,
		role_ids: list[int]
	):
		pass
	
	@staticmethod
	def get_employee_roles(employee_id: int) -> list[Role]:
		pass
