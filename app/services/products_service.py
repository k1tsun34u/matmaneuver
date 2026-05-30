import psycopg
from decimal import Decimal
from app.utils import Utils
from app.models.public.product import Product
from app.types.update_result import UpdateResult
from app.services.base_service import BaseService
from app.types.service_result import ServiceResult
from app.errors.not_found_error import NotFoundError
from app.types.permission_code import PermissionCode
from app.errors.not_allowed_error import NotAllowedError
from app.types.transaction_helper import TransactionHelper
from app.errors.invalid_value_error import InvalidValueError
from app.repositories.public.products_repository import ProductsRepository
from app.repositories.public.employee_permissions_repository import EmployeePermissionsRepository as EPR


class ProductsService(BaseService):
	KEY_HELPERS = (TransactionHelper(Product.ENTITY, Product.TABLE, (Product.COLUMN_NAME,)))
	FKEY_HELPERS = (TransactionHelper(Product.ENTITY, Product.TABLE, (
		Product.COLUMN_DELETED_BY,
		Product.COLUMN_CREATED_BY,
	)),)

	@classmethod
	@BaseService.transaction
	def create(
		cls,
		cur: psycopg.Cursor,
		name: str,
		description: str | None,
		price: Decimal,
		created_by: int | None
	) -> ServiceResult:
		"""
			Errors:
			- InvalidValueError
			- NotAllowedError
			- UnhandledError
		"""

		norm_name = Utils.normalize_name(name)
		if not norm_name:
			return ServiceResult(error=InvalidValueError(Product.ENTITY, Product.COLUMN_NAME))

		if created_by is not None and not EPR.has_permission(cur, created_by, PermissionCode.CREATE_PRODUCT):
			return ServiceResult(error=NotAllowedError(PermissionCode.CREATE_PRODUCT, Product.COLUMN_CREATED_BY))
		
		return ServiceResult(
			result=ProductsRepository.create(
				cur=cur,
				name=norm_name,
				description=description,
				price=price,
				created_by=created_by
			)
		)
	
	@classmethod
	@BaseService.transaction
	def set_description(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		description: str | None,
		set_by: int | None
	) -> ServiceResult:
		"""
			Errors:
			- NotAllowedError
			- NotFoundError
			- UnhandledError
		"""

		if set_by is not None and not EPR.has_permission(cur, set_by, PermissionCode.SET_PRODUCT_DESCRIPTION):
			return ServiceResult(error=NotAllowedError(PermissionCode.SET_PRODUCT_DESCRIPTION))

		if ProductsRepository.set_description(cur, product_id, description) == UpdateResult.FAIL_NOT_FOUND:
			return ServiceResult(error=NotFoundError(Product.ENTITY, Product.COLUMN_ID))
		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def set_price(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		price: Decimal,
		set_by: int | None
	) -> ServiceResult:
		"""
			Errors:
			- InvalidValueError
			- NotFoundError
			- UnhandledError
		"""

		if set_by is not None and not EPR.has_permission(cur, set_by, PermissionCode.SET_PRODUCT_PRICE):
			return ServiceResult(error=NotAllowedError(PermissionCode.SET_PRODUCT_PRICE))

		match ProductsRepository.set_price(cur, product_id, price):
			case UpdateResult.FAIL_CONDITION:
				return ServiceResult(error=InvalidValueError(Product.ENTITY, Product.COLUMN_PRICE))
			case UpdateResult.FAIL_NOT_FOUND:
				return ServiceResult(error=NotFoundError(Product.ENTITY, Product.COLUMN_ID))
		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def soft_delete(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		deleted_by: int | None
	) -> ServiceResult:
		"""
			Errors:
			- NotAllowedError
			- NotFoundError
			- UnhandledError
		"""
		
		if deleted_by is not None and not EPR.has_permission(cur, deleted_by, PermissionCode.DELETE_PRODUCT):
			return ServiceResult(error=NotAllowedError(PermissionCode.DELETE_PRODUCT, Product.COLUMN_DELETED_BY))

		if ProductsRepository.soft_delete(cur, product_id, deleted_by) == UpdateResult.FAIL_NOT_FOUND:
			return ServiceResult(error=NotFoundError(Product.ENTITY, Product.COLUMN_ID))
		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def restore(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		restored_by: int | None
	) -> ServiceResult:
		"""
			Errors:
			- NotAllowedError
			- NotFoundError
			- UnhandledError
		"""
		
		if restored_by is not None and not EPR.has_permission(cur, restored_by, PermissionCode.CREATE_PRODUCT):
			return ServiceResult(error=NotAllowedError(PermissionCode.CREATE_PRODUCT))

		if ProductsRepository.restore(cur, product_id) == UpdateResult.FAIL_NOT_FOUND:
				return ServiceResult(error=NotFoundError(Product.ENTITY, Product.COLUMN_ID))
		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def get_by_id(
		cls,
		cur: psycopg.Cursor,
		product_id: int
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- UnhandledError
		"""

		product = ProductsRepository.get_by_id(cur, product_id)
		if product is None:
			return ServiceResult(error=NotFoundError(Product.ENTITY, Product.COLUMN_ID))
		return ServiceResult(result=product)
	
	@classmethod
	@BaseService.transaction
	def get_many_by_employee_id(
		cls,
		cur: psycopg.Cursor,
		employee_id: int,
		exclude_deleted: bool = True,
		limit: int = 50,
		offset: int = 0
	) -> ServiceResult:
		"""
			Errors:
			- UnhandledError
		"""
		
		return ServiceResult(
			result=ProductsRepository.get_many_by_employee_id(
				cur=cur,
				employee_id=employee_id,
				exclude_deleted=exclude_deleted,
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
		min_price: Decimal | None = None,
		max_price: Decimal | None = None,
		exclude_deleted: bool = True,
		limit: int = 50,
		offset: int = 0
	) -> ServiceResult:
		"""
			Errors:
			- UnhandledError
		"""
		
		return ServiceResult(
			result=ProductsRepository.search(
				cur=cur,
				search=search,
				min_price=min_price,
				max_price=max_price,
				exclude_deleted=exclude_deleted,
				limit=limit,
				offset=offset
			)
		)
