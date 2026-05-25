import psycopg
from datetime import date
from decimal import Decimal
from app.models.public.supply import Supply
from app.types.delete_result import DeleteResult
from app.types.supply_status import SupplyStatus
from app.types.update_result import UpdateResult
from app.services.base_service import BaseService
from app.types.service_result import ServiceResult
from app.errors.not_found_error import NotFoundError
from app.types.permission_code import PermissionCode
from app.models.public.supply_item import SupplyItem
from app.errors.not_allowed_error import NotAllowedError
from app.types.transaction_helper import TransactionHelper
from app.errors.invalid_value_error import InvalidValueError
from app.repositories.public.supplies_repository import SuppliesRepository
from app.repositories.public.supply_items_repository import SupplyItemsRepository
from app.repositories.public.employee_permissions_repository import EmployeePermissionsRepository as EPR
from app.repositories.public.supply_status_history_repository import SupplyStatusHistoryRepository as SSHR


class SuppliesService(BaseService):
	KEY_HELPERS = tuple()
	FKEY_HELPERS = (TransactionHelper(Supply.ENTITY, Supply.TABLE, (
		Supply.COLUMN_SUPPLIER_ID,
		Supply.COLUMN_WAREHOUSE_ID,
		Supply.COLUMN_CREATED_BY,
	)),)

	ALLOWED_STATUS_TRANSITIONS = {
		SupplyStatus.CREATED: (SupplyStatus.CONFIRMED, SupplyStatus.CANCELLED,),
		SupplyStatus.CONFIRMED: (SupplyStatus.IN_TRANSIT, SupplyStatus.CANCELLED,),
		SupplyStatus.IN_TRANSIT: (SupplyStatus.DELIVERED,),
		SupplyStatus.DELIVERED: tuple(),
		SupplyStatus.CANCELLED: tuple()
	}

	ALLOWED_ITEM_EDIT_STATUSES = (SupplyStatus.CREATED,)

	@classmethod
	@BaseService.transaction
	def create(
		cls,
		cur: psycopg.Cursor,
		supplier_id: int,
		warehouse_id: int,
		planned_delivery_date: date,
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

		if planned_delivery_date < date.today():
			return ServiceResult(error=InvalidValueError(Supply.ENTITY, Supply.COLUMN_PLANNED_DELIVERY_DATE))

		if created_by is not None and not EPR.has_permission(cur, created_by, PermissionCode.CREATE_SUPPLY):
			return ServiceResult(error=NotAllowedError(PermissionCode.CREATE_SUPPLY, Supply.COLUMN_CREATED_BY))
		
		supply_id = SuppliesRepository.create(
			cur=cur,
			supplier_id=supplier_id,
			warehouse_id=warehouse_id,
			planned_delivery_date=planned_delivery_date,
			created_by=created_by
		)

		latest_status_id = SSHR.create(cur, supply_id, SupplyStatus.CREATED, created_by)
		return ServiceResult(result=(supply_id, latest_status_id,))
	
	@classmethod
	@BaseService.transaction
	def set_status(
		cls,
		cur: psycopg.Cursor,
		supply_id: int,
		status: SupplyStatus,
		set_by: int | None
	) -> ServiceResult:
		"""
			Errors:
			- NotAllowedError
			- InvalidValueError
			- NotFoundError
			- UnhandledError
		"""

		if set_by is not None and not EPR.has_permission(cur, set_by, PermissionCode.SET_SUPPLY_STATUS):
			return ServiceResult(error=NotAllowedError(PermissionCode.SET_SUPPLY_STATUS, Supply.COLUMN_CURRENT_STATUS))
		
		supply = SuppliesRepository.get_by_id_for_update(cur, supply_id)
		if supply is None:
			return ServiceResult(error=NotFoundError(Supply.ENTITY, Supply.COLUMN_ID))
		
		if status not in cls.ALLOWED_STATUS_TRANSITIONS[supply.current_status]:
			return ServiceResult(error=InvalidValueError(Supply.ENTITY, Supply.COLUMN_CURRENT_STATUS))
		
		changed = SuppliesRepository.set_status(
			cur=cur,
			supply_id=supply_id,
			status=status
		)

		if changed == UpdateResult.FAIL_NOT_FOUND:
			return ServiceResult(error=NotFoundError(Supply.ENTITY, Supply.COLUMN_ID))
		
		return ServiceResult(result=SSHR.create(cur, supply_id, status, set_by))
	
	@classmethod
	@BaseService.transaction
	def get_by_id(
		cls,
		cur: psycopg.Cursor,
		supply_id: int
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- UnhandledError
		"""

		supply = SuppliesRepository.get_by_id(cur, supply_id)
		if not supply:
			return ServiceResult(error=NotFoundError(Supply.ENTITY, Supply.COLUMN_ID))
		return ServiceResult(result=supply)
	
	@classmethod
	@BaseService.transaction
	def get_many_by_supplier_id(
		cls,
		cur: psycopg.Cursor,
		supplier_id: int,
		limit: int = 50,
		offset: int = 0
	) -> ServiceResult:
		"""
			Errors:
			- UnhandledError
		"""

		
		return ServiceResult(
			result=SuppliesRepository.get_many_by_supplier_id(
				cur=cur,
				supplier_id=supplier_id,
				limit=limit,
				offset=offset
			)
		)
	
	@classmethod
	@BaseService.transaction
	def get_many_by_warehouse_id(
		cls,
		cur: psycopg.Cursor,
		warehouse_id: int,
		limit: int = 50,
		offset: int = 0
	) -> ServiceResult:
		"""
			Errors:
			- UnhandledError
		"""

		return ServiceResult(
			result=SuppliesRepository.get_many_by_warehouse_id(
				cur=cur,
				warehouse_id=warehouse_id,
				limit=limit,
				offset=offset
			)
		)

	@classmethod
	@BaseService.transaction
	def create_item(
		cls,
		cur: psycopg.Cursor,
		supply_id: int,
		product_id: int,
		quantity: int,
		price: Decimal,
		created_by: int | None
	) -> ServiceResult:
		"""
			Errors:
			- NotAllowedError
			- AlreadyExistsError
			- NotFoundError
			- UnhandledError
		"""

		if created_by is not None and not EPR.has_permission(cur, created_by, PermissionCode.CREATE_SUPPLY_ITEM):
			return ServiceResult(error=NotAllowedError(PermissionCode.CREATE_SUPPLY_ITEM))
		
		supply = SuppliesRepository.get_by_id_for_update(cur, supply_id)
		if supply is None:
			return ServiceResult(error=NotFoundError(Supply.ENTITY, Supply.COLUMN_ID))
		
		if supply.current_status not in cls.ALLOWED_ITEM_EDIT_STATUSES:
			return ServiceResult(error=InvalidValueError(Supply.ENTITY, Supply.COLUMN_CURRENT_STATUS))
		
		return ServiceResult(
			result=SupplyItemsRepository.create(
				cur=cur,
				supply_id=supply_id,
				product_id=product_id,
				quantity=quantity,
				price=price
			)
		)
	
	@classmethod
	@BaseService.transaction
	def delete_item(
		cls,
		cur: psycopg.Cursor,
		supply_item_id: int,
		deleted_by: int | None
	) -> ServiceResult:
		"""
			Errors:
			- NotAllowedError
			- NotFoundError
			- UnhandledError
		"""

		if deleted_by is not None and not EPR.has_permission(cur, deleted_by, PermissionCode.DELETE_SUPPLY_ITEM):
			return ServiceResult(error=NotAllowedError(PermissionCode.DELETE_SUPPLY_ITEM))
		
		supply_item = SupplyItemsRepository.get_by_id(cur, supply_item_id)
		if supply_item is None:
			return ServiceResult(error=NotFoundError(SupplyItem.ENTITY, SupplyItem.COLUMN_ID))
		
		supply = SuppliesRepository.get_by_id_for_update(cur, supply_item.supply_id)
		if supply is None:
			return ServiceResult(error=NotFoundError(Supply.ENTITY, Supply.COLUMN_ID))
		
		if supply.current_status not in cls.ALLOWED_ITEM_EDIT_STATUSES:
			return ServiceResult(error=InvalidValueError(Supply.ENTITY, Supply.COLUMN_CURRENT_STATUS))

		if SupplyItemsRepository.delete(cur, supply_item_id) == DeleteResult.FAIL_NOT_FOUND:
			return ServiceResult(error=NotFoundError(SupplyItem.ENTITY, SupplyItem.COLUMN_ID))
		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def get_item_by_id(
		cls,
		cur: psycopg.Cursor,
		supply_item_id: int
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- UnhandledError
		"""

		supply_item = SupplyItemsRepository.get_by_id(cur, supply_item_id)
		if not supply_item:
			return ServiceResult(error=NotFoundError(SupplyItem.ENTITY, SupplyItem.COLUMN_ID))
		return ServiceResult(result=supply_item)
	
	@classmethod
	@BaseService.transaction
	def get_items_by_supply_id(
		cls,
		cur: psycopg.Cursor,
		supply_id: int,
		limit: int = 50,
		offset: int = 0
	) -> ServiceResult:
		"""
			Errors:
			- UnhandledError
		"""

		return ServiceResult(
			result=SupplyItemsRepository.get_many_by_supply_id(
				cur=cur,
				supply_id=supply_id,
				limit=limit,
				offset=offset
			)
		)
	
	@classmethod
	@BaseService.transaction
	def get_items_by_product_id(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		limit: int = 50,
		offset: int = 0
	) -> ServiceResult:
		"""
			Errors:
			- UnhandledError
		"""

		return ServiceResult(
			result=SupplyItemsRepository.get_many_by_product_id(
				cur=cur,
				product_id=product_id,
				limit=limit,
				offset=offset
			)
		)
	
	@classmethod
	@BaseService.transaction
	def get_products_by_supply_id(
		cls,
		cur: psycopg.Cursor,
		supply_id: int
	) -> ServiceResult:
		"""
			Errors:
			- UnhandledError
		"""

		return ServiceResult(
			result=SupplyItemsRepository.get_products_by_supply_id(cur, supply_id)
		)
	
	@classmethod
	@BaseService.transaction
	def get_status_history(
		cls,
		cur: psycopg.Cursor,
		supply_id: int,
		limit: int = 50,
		offset: int = 0
	) -> ServiceResult:
		"""
			Errors:
			- UnhandledError
		"""

		return ServiceResult(
			result=SSHR.get_many_by_supply_id(
				cur=cur,
				supply_id=supply_id,
				limit=limit,
				offset=offset
			)
		)
