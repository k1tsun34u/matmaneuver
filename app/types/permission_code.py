from enum import StrEnum


class PermissionCode(StrEnum):
	CREATE_USER = "create_user"
	BLOCK_USER = "block_user"
	UNBLOCK_USER = "unblock_user"
	DELETE_USER = "delete_user"

	HIRE_EMPLOYEE = "hire"
	FIRE_EMPLOYEE = "fire"
	CREATE_EMPLOYEE = "create_employee"

	CREATE_PERMISSION = "create_permission"
	DEACTIVATE_PERMISSION = "deactivate_permission"