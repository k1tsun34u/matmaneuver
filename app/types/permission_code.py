from enum import StrEnum


class PermissionCode(StrEnum):
	CREATE_USER = "create_user"
	BLOCK_USER = "block_user"
	UNBLOCK_USER = "unblock_user"
	DELETE_USER = "delete_user"

	CREATE_EMPLOYEE = "create_employee"
	HIRE_EMPLOYEE = "hire"
	FIRE_EMPLOYEE = "fire"

	CREATE_PERMISSION = "create_permission"
	ASSIGN_PERMISSION = "assign_permission"
	UNASSIGN_PERMISSION = "unassign_permission"
	DEACTIVATE_PERMISSION = "deactivate_permission"
	
	CREATE_ROLE = "create_role"
	DEACTIVATE_ROLE = "deactivate_role"
	ASSIGN_ROLE = "assign_role"
	UNASSIGN_ROLE = "unassign_role"
