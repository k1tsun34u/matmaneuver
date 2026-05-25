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
	SET_PERMISSION_DESCRIPTION = "set_permission_description"
	
	CREATE_ROLE = "create_role"
	DEACTIVATE_ROLE = "deactivate_role"
	ASSIGN_ROLE = "assign_role"
	UNASSIGN_ROLE = "unassign_role"

	CREATE_WAREHOUSE = "create_warehouse"
	DELETE_WAREHOUSE = "delete_warehouse"
	SET_WAREHOUSE_DESCRIPTION = "set_warehouse_description"
	ADD_WAREHOUSE_PRODUCT = "add_warehouse_product"
	DELETE_WAREHOUSE_PRODUCT = "delete_warehouse_product"

	CREATE_PRODUCT = "create_product"
	DELETE_PRODUCT = "delete_product"
	SET_PRODUCT_PRICE = "set_product_price"
	SET_PRODUCT_DESCRIPTION = "set_product_description"

	ASSIGN_PRODUCT_CATEGORY = "assign_product_category"
	UNASSIGN_PRODUCT_CATEGORY = "unassign_product_category"
	CREATE_PRODUCT_IMAGE = "create_product_image"
	DELETE_PRODUCT_IMAGE = "delete_product_image"

	CREATE_SUPPLIER = "create_supplier"
	DEACTIVATE_SUPPLIER = "deactivate_supplier"
	SET_SUPPLIER_FIELDS = "set_supplier_fields"

	CREATE_SUPPLY = "create_supply"
	SET_SUPPLY_STATUS = "set_supply_status"

	CREATE_SUPPLY_ITEM = "create_supply_item"
	
