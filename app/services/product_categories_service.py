import psycopg
from collections.abc import Sequence
from app.errors.not_allowed_error import NotAllowedError
from app.services.base_service import BaseService
from app.types.permission_code import PermissionCode
from app.types.service_result import ServiceResult
from app.errors.not_found_error import NotFoundError
from app.types.transaction_helper import TransactionHelper
from app.models.public.product_category import ProductCategory
from app.repositories.public.product_categories_repository import ProductCategoriesRepository
from app.repositories.public.employee_permissions_repository import EmployeePermissionsRepository as EPR


class ProductCategoriesService(BaseService):
	KEY_HELPERS = tuple()
	FKEY_HELPERS = (TransactionHelper(ProductCategory.ENTITY, ProductCategory.TABLE, (ProductCategory.COLUMN_ASSIGNED_BY,)),)

	@classmethod
	@BaseService.transaction
	def assign_many(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		category_ids: Sequence[int],
		assigned_by: int | None
	) -> ServiceResult:
		"""
			Errors:
			- NotAllowedError
			- NotFoundError
			- UnhandledError
		"""

		if assigned_by is not None and not EPR.has_permission(cur, assigned_by, PermissionCode.ASSIGN_PRODUCT_CATEGORY):
			return ServiceResult(error=NotAllowedError(PermissionCode.ASSIGN_PRODUCT_CATEGORY, ProductCategory.COLUMN_ASSIGNED_BY))

		ProductCategoriesRepository.assign_many(
			cur=cur,
			product_id=product_id,
			category_ids=category_ids,
			assigned_by=assigned_by
		)

		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def unassign_many(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		category_ids: Sequence[int],
		unassigned_by: int | None
	) -> ServiceResult:
		"""
			Errors:
			- NotAllowedError
			- NotFoundError
			- UnhandledError

		"""
		
		if unassigned_by is not None and not EPR.has_permission(cur, unassigned_by, PermissionCode.UNASSIGN_PRODUCT_CATEGORY):
			return ServiceResult(error=NotAllowedError(PermissionCode.UNASSIGN_PRODUCT_CATEGORY))

		ProductCategoriesRepository.unassign_many(
			cur=cur,
			product_id=product_id,
			category_ids=category_ids
		)

		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def get_by_product_id_category_id(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		category_id: int
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- UnhandledError
		"""

		relation = ProductCategoriesRepository.get_by_product_id_category_id(
			cur=cur,
			product_id=product_id,
			category_id=category_id
		)

		if relation is None:
			return ServiceResult(error=NotFoundError(ProductCategory.ENTITY, ProductCategory.COLUMN_PRODUCT_ID))
		return ServiceResult(result=relation)
	
	@classmethod
	@BaseService.transaction
	def get_categories_by_product_id(
		cls,
		cur: psycopg.Cursor,
		product_id: int
	) -> ServiceResult:
		"""
			Errors:
			- UnhandledError
		"""

		return ServiceResult(
			result=ProductCategoriesRepository.get_categories_by_product_id(cur, product_id)
		)
	
	@classmethod
	@BaseService.transaction
	def get_products_by_category_id(
		cls,
		cur: psycopg.Cursor,
		category_id: int,
		limit: int = 50,
		offset: int = 0
	) -> ServiceResult:
		"""
			Errors:
			- UnhandledError
		"""

		return ServiceResult(
			result=ProductCategoriesRepository.get_products_by_category_id(
				cur=cur,
				category_id=category_id,
				limit=limit,
				offset=offset
			)
		)
