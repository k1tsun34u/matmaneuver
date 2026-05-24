import psycopg
from collections.abc import Sequence
from app.types.delete_result import DeleteResult
from app.types.update_result import UpdateResult
from app.models.public.warehouse import Warehouse
from app.services.base_service import BaseService
from app.types.service_result import ServiceResult
from app.errors.not_found_error import NotFoundError
from app.types.permission_code import PermissionCode
from app.errors.not_allowed_error import NotAllowedError
from app.types.transaction_helper import TransactionHelper
from app.errors.invalid_value_error import InvalidValueError
from app.models.public.warehouse_product import WarehouseProduct
from app.repositories.public.warehouses_repository import WarehousesRepository
from app.repositories.public.warehouse_products_repository import WarehouseProductsRepository as WPR
from app.repositories.public.employee_permissions_repository import EmployeePermissionsRepository as EPR


class WarehousesService(BaseService):
	KEY_HELPERS = (TransactionHelper(Warehouse.ENTITY, Warehouse.TABLE, (Warehouse.COLUMN_ADDRESS,)),)
	FKEY_HELPERS = (TransactionHelper(Warehouse.ENTITY, Warehouse.TABLE, (
		Warehouse.COLUMN_DELETED_BY,
		Warehouse.COLUMN_CREATED_BY,
	)),)

	@classmethod
	@BaseService.transaction
	def create(
		cls,
		cur: psycopg.Cursor,
		address: str,
		description: str | None,
		created_by: int | None
	) -> ServiceResult:
		"""
			Errors:
			- NotAllowedError
			- NotFoundError
			- AlreadyExistsError
			- UnhandledError
		"""

		if created_by is not None and not EPR.has_permission(cur, created_by, PermissionCode.CREATE_WAREHOUSE):
			return ServiceResult(error=NotAllowedError(PermissionCode.CREATE_WAREHOUSE, Warehouse.COLUMN_CREATED_BY))
		
		return ServiceResult(
			result=WarehousesRepository.create(
				cur=cur,
				address=address,
				description=description,
				created_by=created_by
			)
		)
	
	@classmethod
	@BaseService.transaction
	def set_description(
		cls,
		cur: psycopg.Cursor,
		warehouse_id: int,
		description: str | None,
		set_by: int | None
	) -> ServiceResult:
		"""
			Errors:
			- NotAllowedError
			- NotFoundError
			- UnhandledError
		"""

		if set_by is not None and not EPR.has_permission(cur, set_by, PermissionCode.SET_WAREHOUSE_DESCRIPTION):
			return ServiceResult(error=NotAllowedError(PermissionCode.SET_WAREHOUSE_DESCRIPTION))
		
		if WarehousesRepository.set_description(cur, warehouse_id, description) == UpdateResult.FAIL_NOT_FOUND:
			return ServiceResult(error=NotFoundError(Warehouse.ENTITY, Warehouse.COLUMN_ID))
		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def soft_delete(
		cls,
		cur: psycopg.Cursor,
		warehouse_id: int,
		deleted_by: int | None
	) -> ServiceResult:
		"""
			Errors:
			- NotAllowedError
			- NotFoundError
			- UnhandledError
		"""

		if deleted_by is not None and not EPR.has_permission(cur, deleted_by, PermissionCode.DELETE_WAREHOUSE):
			return ServiceResult(error=NotAllowedError(PermissionCode.DELETE_WAREHOUSE, Warehouse.COLUMN_DELETED_BY))
		
		if WarehousesRepository.soft_delete(cur, warehouse_id, deleted_by) == UpdateResult.FAIL_NOT_FOUND:
			return ServiceResult(error=NotFoundError(Warehouse.ENTITY, Warehouse.COLUMN_ID))
		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def restore(
		cls,
		cur: psycopg.Cursor,
		warehouse_id: int,
		restored_by: int | None
	) -> ServiceResult:
		"""
			Errors:
			- NotAllowedError
			- NotFoundError
			- UnhandledError
		"""

		if restored_by is not None and not EPR.has_permission(cur, restored_by, PermissionCode.CREATE_WAREHOUSE):
			return ServiceResult(error=NotAllowedError(PermissionCode.CREATE_WAREHOUSE))
		
		if WarehousesRepository.restore(cur, warehouse_id) == UpdateResult.FAIL_NOT_FOUND:
			return ServiceResult(error=NotFoundError(Warehouse.ENTITY, Warehouse.COLUMN_ID))
		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def get_by_id(
		cls,
		cur: psycopg.Cursor,
		warehouse_id: int
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- UnhandledError
		"""

		warehouse = WarehousesRepository.get_by_id(cur, warehouse_id)
		if not warehouse:
			return ServiceResult(error=NotFoundError(Warehouse.ENTITY, Warehouse.COLUMN_ID))
		return ServiceResult(result=warehouse)
	
	@classmethod
	@BaseService.transaction
	def get_by_address(
		cls,
		cur: psycopg.Cursor,
		address: str
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- UnhandledError
		"""

		warehouse = WarehousesRepository.get_by_address(cur, address)
		if not warehouse:
			return ServiceResult(error=NotFoundError(Warehouse.ENTITY, Warehouse.COLUMN_ADDRESS))
		return ServiceResult(result=warehouse)
	
	@classmethod
	@BaseService.transaction
	def search(
		cls,
		cur: psycopg.Cursor,
		search: str | None = None,
		exclude_deleted: bool = True,
		limit: int = 50,
		offset: int = 0
	) -> ServiceResult:
		"""
			Errors:
			- UnhandledError
		"""

		return ServiceResult(
			result=WarehousesRepository.search(
				cur=cur,
				search=search,
				exclude_deleted=exclude_deleted,
				limit=limit,
				offset=offset
			)
		)

	@classmethod
	@BaseService.transaction
	def add_product(
		cls,
		cur: psycopg.Cursor,
		warehouse_id: int,
		product_id: int,
		added_by: int | None
	) -> ServiceResult:
		"""
			Errors:
			- NotAllowedError
			- AlreadyExistsError
			- NotFoundError
			- UnhandledError
		"""

		if added_by is not None and not EPR.has_permission(cur, added_by, PermissionCode.ADD_WAREHOUSE_PRODUCT):
			return ServiceResult(error=NotAllowedError(PermissionCode.ADD_WAREHOUSE_PRODUCT, WarehouseProduct.COLUMN_CREATED_BY))
		
		WPR.create(cur, product_id, warehouse_id, added_by)
		return ServiceResult()

	@classmethod
	@BaseService.transaction
	def delete_product(
		cls,
		cur: psycopg.Cursor,
		warehouse_id: int,
		product_id: int,
		deleted_by: int | None
	) -> ServiceResult:
		"""
			Errors:
			- NotAllowedError
			- NotFoundError
			- UnhandledError
		"""

		if deleted_by is not None and not EPR.has_permission(cur, deleted_by, PermissionCode.DELETE_WAREHOUSE_PRODUCT):
			return ServiceResult(error=NotAllowedError(PermissionCode.DELETE_WAREHOUSE_PRODUCT))
		
		match WPR.delete(cur, product_id, warehouse_id):
			case DeleteResult.FAIL_CONDITION:
				return ServiceResult(error=InvalidValueError(WarehouseProduct.ENTITY, WarehouseProduct.COLUMN_QUANTITY))
			case DeleteResult.FAIL_NOT_FOUND:
				return ServiceResult(error=NotFoundError(WarehouseProduct.ENTITY))
		return ServiceResult()

	@classmethod
	@BaseService.transaction
	def delete_all_products(
		cls,
		cur: psycopg.Cursor,
		warehouse_id: int,
		deleted_by: int | None
	) -> ServiceResult:
		"""
			Errors:
			- NotAllowedError
			- NotFoundError
			- UnhandledError
		"""

		if deleted_by is not None and not EPR.has_permission(cur, deleted_by, PermissionCode.DELETE_WAREHOUSE_PRODUCT):
			return ServiceResult(error=NotAllowedError(PermissionCode.DELETE_WAREHOUSE_PRODUCT))
		
		match WPR.delete_many_by_warehouse_id(cur, warehouse_id):
			case DeleteResult.FAIL_CONDITION:
				return ServiceResult(error=InvalidValueError(WarehouseProduct.ENTITY, WarehouseProduct.COLUMN_QUANTITY))
			case DeleteResult.FAIL_NOT_FOUND:
				return ServiceResult(error=NotFoundError(WarehouseProduct.ENTITY))
		return ServiceResult()

	@classmethod
	@BaseService.transaction
	def increase_product_quantity(
		cls,
		cur: psycopg.Cursor,
		warehouse_id: int,
		product_id: int,
		quantity: int,
		increased_by: int | None
	) -> ServiceResult:
		"""
			Errors:
			- NotAllowedError
			- InvalidValueError
			- NotFoundError
			- UnhandledError
		"""

		if increased_by is not None and not EPR.has_permission(cur, increased_by, PermissionCode.ADD_WAREHOUSE_PRODUCT):
			return ServiceResult(error=NotAllowedError(PermissionCode.ADD_WAREHOUSE_PRODUCT))
		
		match WPR.increase_quantity(cur, product_id, warehouse_id, quantity):
			case UpdateResult.FAIL_CONDITION:
				return ServiceResult(error=InvalidValueError(WarehouseProduct.ENTITY, WarehouseProduct.COLUMN_QUANTITY))
			case UpdateResult.FAIL_NOT_FOUND:
				return ServiceResult(error=NotFoundError(WarehouseProduct.ENTITY))
		return ServiceResult()

	@classmethod
	@BaseService.transaction
	def decrease_product_quantity(
		cls,
		cur: psycopg.Cursor,
		warehouse_id: int,
		product_id: int,
		quantity: int,
		decreased_by: int | None
	) -> ServiceResult:
		"""
			Errors:
			- NotAllowedError
			- InvalidValueError
			- NotFoundError
			- UnhandledError
		"""

		if decreased_by is not None and not EPR.has_permission(cur, decreased_by, PermissionCode.DELETE_WAREHOUSE_PRODUCT):
			return ServiceResult(error=NotAllowedError(PermissionCode.DELETE_WAREHOUSE_PRODUCT))
		
		match WPR.decrease_quantity(cur, product_id, warehouse_id, quantity):
			case UpdateResult.FAIL_CONDITION:
				return ServiceResult(error=InvalidValueError(Warehouse.ENTITY, WarehouseProduct.COLUMN_QUANTITY))
			case UpdateResult.FAIL_NOT_FOUND:
				return ServiceResult(error=NotFoundError(WarehouseProduct.ENTITY))
		return ServiceResult()

	@classmethod
	@BaseService.transaction
	def reserve_product(
		cls,
		cur: psycopg.Cursor,
		warehouse_id: int,
		product_id: int,
		reserve_quantity: int
	) -> ServiceResult:
		"""
			Errors:
			- InvalidValueError
			- NotFoundError
			- UnhandledError
		"""
		
		match WPR.reserve(cur, product_id, warehouse_id, reserve_quantity):
			case UpdateResult.FAIL_CONDITION:
				return ServiceResult(error=InvalidValueError(WarehouseProduct.ENTITY, WarehouseProduct.COLUMN_RESERVED_QUANTITY))
			case UpdateResult.FAIL_NOT_FOUND:
				return ServiceResult(error=NotFoundError(WarehouseProduct.ENTITY))
		return ServiceResult()

	@classmethod
	@BaseService.transaction
	def unreserve_product(
		cls,
		cur: psycopg.Cursor,
		warehouse_id: int,
		product_id: int,
		reserve_quantity: int
	) -> ServiceResult:
		"""
			Errors:
			- InvalidValueError
			- NotFoundError
			- UnhandledError
		"""
		
		match WPR.unreserve(cur, product_id, warehouse_id, reserve_quantity):
			case UpdateResult.FAIL_CONDITION:
				return ServiceResult(error=InvalidValueError(WarehouseProduct.ENTITY, WarehouseProduct.COLUMN_RESERVED_QUANTITY))
			case UpdateResult.FAIL_NOT_FOUND:
				return ServiceResult(error=NotFoundError(WarehouseProduct.ENTITY))
		return ServiceResult()

	@classmethod
	@BaseService.transaction
	def consume_product(
		cls,
		cur: psycopg.Cursor,
		warehouse_id: int,
		product_id: int,
		quantity: int
	) -> ServiceResult:
		"""
			Errors:
			- InvalidValueError
			- NotFoundError
			- UnhandledError
		"""
		
		match WPR.consume(cur, product_id, warehouse_id, quantity):
			case UpdateResult.FAIL_CONDITION:
				return ServiceResult(error=InvalidValueError(WarehouseProduct.ENTITY, WarehouseProduct.COLUMN_QUANTITY))
			case UpdateResult.FAIL_NOT_FOUND:
				return ServiceResult(error=NotFoundError(WarehouseProduct.ENTITY))
		return ServiceResult()

	@classmethod
	@BaseService.transaction
	def get_products(
		cls,
		cur: psycopg.Cursor,
		warehouse_id: int
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- UnhandledError
		"""

		return ServiceResult(result=WPR.get_many_by_warehouse_id(cur, warehouse_id))
