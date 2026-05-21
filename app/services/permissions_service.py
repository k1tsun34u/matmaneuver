
from app.db import Db
from app.utils import Utils
from app.errors.other import InternalError
from app.repositories.public.employees_repository import EmployeesRepository
from app.repositories.public.permissions_repository import PermissionsRepository
from app.errors.validation import (
	InvalidCodeError
)
from app.errors.user import (
	EmployeeNotFoundError,

	PermissionCodeAlreadyExistsError,
	PermissionNotFoundError
)


class PermissionsService:
	@staticmethod
	def create_permission(
		code: str,
		description: str | None,
		is_system: bool,
		created_by: int
	) -> int:
		pass

	@staticmethod
	def deactivate_permission(permission_id: int, deactivated_by: int):
		pass

	@staticmethod
	def restore_permission(permission_id: int):
		pass
