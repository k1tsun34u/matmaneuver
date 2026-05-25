import psycopg
from decimal import Decimal
from app.models.public.supply import Supply
from app.types.supply_status import SupplyStatus
from app.services.base_service import BaseService
from app.types.service_result import ServiceResult
from app.errors.not_found_error import NotFoundError
from app.types.permission_code import PermissionCode
from app.models.public.supply_item import SupplyItem
from app.errors.not_allowed_error import NotAllowedError
from app.types.transaction_helper import TransactionHelper
from app.repositories.public.supplies_repository import SuppliesRepository
from app.repositories.public.supply_items_repository import SupplyItemsRepository
from app.repositories.public.employee_permissions_repository import EmployeePermissionsRepository as EPR


class SupplyItemsService(BaseService):
	KEY_HELPERS = tuple()
	FKEY_HELPERS = (TransactionHelper(SupplyItem.ENTITY, SupplyItem.TABLE, (
		SupplyItem.COLUMN_SUPPLY_ID,
		SupplyItem.COLUMN_PRODUCT_ID,
	)),)

	ALLOWED_ITEM_EDIT_STATUSES = (SupplyStatus.CREATED,)

	@classmethod
	@BaseService.transaction
	def create(
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
			return ServiceResult(error=NotAllowedError(PermissionCode.CREATE_SUPPLY_ITEM))
		
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
	def get_by_id(
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
	def get_many_by_supply_id(
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
	def get_many_by_product_id(
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
