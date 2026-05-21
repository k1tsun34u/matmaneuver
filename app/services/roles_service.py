
from app.db import Db
from app.utils import Utils
from app.errors.other import InternalError
from app.models.public.permission import Permission
from app.repositories.public.roles_repository import RolesRepository
from app.repositories.public.employees_repository import EmployeesRepository
from app.repositories.public.permissions_repository import PermissionsRepository
from app.repositories.public.role_permissions_repository import RolePermissionsRepository
from app.errors.validation import InvalidCodeError
from app.errors.user import (
	EmployeeNotFoundError,

	RoleCodeAlreadyExistsError,
	RoleNotFoundError,

	PermissionNotFoundError
)


class RolesService:
	@staticmethod
	def create_role(
		code: str,
		is_system: bool,
		created_by: int | None
	) -> int:
		pass

	@staticmethod
	def deactivate_role(role_id: int, deactivated_by: int):
		pass

	@staticmethod
	def restore_role(role_id: int):
		pass
	
	@staticmethod
	def assign_role_permissions(
		role_id: int,
		permission_ids: list[int],
		assigned_by: int | None
	):
		pass
	
	@staticmethod
	def unassign_role_permissions(role_id: int, permission_ids: list[int]):
		pass
	
	@staticmethod
	def get_role_permissions(role_id: int) -> list[Permission]:
		pass
