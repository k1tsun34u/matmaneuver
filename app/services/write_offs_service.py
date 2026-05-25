import psycopg
from datetime import date
from app.models.public.product import Product
from app.models.public.write_off import WriteOff
from app.services.base_service import BaseService
from app.types.service_result import ServiceResult
from app.errors.not_found_error import NotFoundError
from app.types.permission_code import PermissionCode
from app.types.write_off_reason import WriteOffReason
from app.errors.not_allowed_error import NotAllowedError
from app.models.public.write_off_item import WriteOffItem
from app.types.transaction_helper import TransactionHelper
from app.repositories.public.products_repository import ProductsRepository
from app.repositories.public.write_offs_repository import WriteOffsRepository
from app.repositories.public.write_off_items_repository import WriteOffItemsRepository as WOIR
from app.repositories.public.employee_permissions_repository import EmployeePermissionsRepository as EPR


class WriteOffsService(BaseService):
	KEY_HELPERS = tuple()
	FKEY_HELPERS = (
		TransactionHelper(WriteOff.ENTITY, WriteOff.TABLE, (
			WriteOff.COLUMN_WAREHOUSE_ID,
			WriteOff.COLUMN_CREATED_BY,
		)),
		TransactionHelper(WriteOffItem.ENTITY, WriteOffItem.TABLE, (
			WriteOffItem.COLUMN_WRITE_OFF_ID,
			WriteOffItem.COLUMN_PRODUCT_ID,
		)),
	)

	@classmethod
	@BaseService.transaction
	def create(
		cls,
		cur: psycopg.Cursor,
		warehouse_id: int,
		reason: WriteOffReason,
		comment: str | None,
		created_by: int | None
	) -> ServiceResult:
		"""
			Errors:
			- NotAllowedError
			- NotFoundError
			- UnhandledError
		"""

		if created_by is not None and not EPR.has_permission(cur, created_by, PermissionCode.CREATE_WRITE_OFF):
			return ServiceResult(error=NotAllowedError(PermissionCode.CREATE_WRITE_OFF, WriteOff.COLUMN_CREATED_BY))
		
		write_off_id = WriteOffsRepository.create(
			cur=cur,
			warehouse_id=warehouse_id,
			reason=reason,
			comment=comment,
			created_by=created_by
		)

		return ServiceResult(result=write_off_id)
	
	@classmethod
	@BaseService.transaction
	def get_by_id(
		cls,
		cur: psycopg.Cursor,
		write_off_id: int
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- UnhandledError
		"""

		write_off = WriteOffsRepository.get_by_id(cur, write_off_id)
		if not write_off:
			return ServiceResult(error=NotFoundError(WriteOff.ENTITY, WriteOff.COLUMN_ID))
		return ServiceResult(result=write_off)
	
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
			result=WriteOffsRepository.get_many_by_warehouse_id(
				cur=cur,
				warehouse_id=warehouse_id,
				limit=limit,
				offset=offset
			)
		)
	
	@classmethod
	@BaseService.transaction
	def search(
		cls,
		cur: psycopg.Cursor,
		search: str | None = None,
		warehouse_id: int | None = None,
		reason: WriteOffReason | None = None,
		created_from: date | None = None,
		created_to: date | None = None,
		limit: int = 50,
		offset: int = 0
	) -> ServiceResult:
		"""
			Errors:
			- UnhandledError
		"""

		return ServiceResult(
			result=WriteOffsRepository.search(
				cur=cur,
				search=search,
				warehouse_id=warehouse_id,
				reason=reason,
				created_from=created_from,
				created_to=created_to,
				limit=limit,
				offset=offset
			)
		)

	@classmethod
	@BaseService.transaction
	def create_item(
		cls,
		cur: psycopg.Cursor,
		write_off_id: int,
		product_id: int,
		quantity: int,
		created_by: int | None
	) -> ServiceResult:
		"""
			Errors:
			- NotAllowedError
			- AlreadyExistsError
			- NotFoundError
			- UnhandledError
		"""

		if created_by is not None and not EPR.has_permission(cur, created_by, PermissionCode.CREATE_WRITE_OFF_ITEM):
			return ServiceResult(error=NotAllowedError(PermissionCode.CREATE_WRITE_OFF_ITEM))
		
		write_off = WriteOffsRepository.get_by_id(cur, write_off_id)
		if write_off is None:
			return ServiceResult(error=NotFoundError(WriteOff.ENTITY, WriteOff.COLUMN_ID))
		
		product = ProductsRepository.get_by_id(cur, product_id)
		if product is None:
			return ServiceResult(error=NotFoundError(Product.ENTITY, Product.COLUMN_ID))
		
		return ServiceResult(
			result=WOIR.create(
				cur=cur,
				write_off_id=write_off_id,
				product_id=product_id,
				quantity=quantity,
				price=product.price
			)
		)
	
	@classmethod
	@BaseService.transaction
	def get_item_by_id(
		cls,
		cur: psycopg.Cursor,
		write_off_item_id: int
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- UnhandledError
		"""

		write_off_item = WOIR.get_by_id(cur, write_off_item_id)
		if not write_off_item:
			return ServiceResult(error=NotFoundError(WriteOffItem.ENTITY, WriteOffItem.COLUMN_ID))
		return ServiceResult(result=write_off_item)
	
	@classmethod
	@BaseService.transaction
	def get_items_by_write_off_id(
		cls,
		cur: psycopg.Cursor,
		write_off_id: int,
		limit: int = 50,
		offset: int = 0
	) -> ServiceResult:
		"""
			Errors:
			- UnhandledError
		"""

		return ServiceResult(
			result=WOIR.get_many_by_write_off_id(
				cur=cur,
				write_off_id=write_off_id,
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
			result=WOIR.get_many_by_product_id(
				cur=cur,
				product_id=product_id,
				limit=limit,
				offset=offset
			)
		)
