import psycopg
from app.utils import Utils
from app.models.public.category import Category
from app.types.update_result import UpdateResult
from app.services.base_service import BaseService
from app.types.service_result import ServiceResult
from app.errors.not_found_error import NotFoundError
from app.types.permission_code import PermissionCode
from app.errors.not_allowed_error import NotAllowedError
from app.types.transaction_helper import TransactionHelper
from app.errors.invalid_value_error import InvalidValueError
from app.repositories.public.categories_repository import CategoriesRepository
from app.repositories.public.employee_permissions_repository import EmployeePermissionsRepository as EPR


class CategoriesService(BaseService):
	KEY_HELPERS = (TransactionHelper(Category.ENTITY, Category.TABLE, (Category.COLUMN_NAME,)),)
	FKEY_HELPERS = (TransactionHelper(Category.ENTITY, Category.TABLE, (
		Category.COLUMN_PARENT_CATEGORY_ID,
		Category.COLUMN_DEACTIVATED_BY,
		Category.COLUMN_CREATED_BY,
	)),)

	@classmethod
	@BaseService.transaction
	def create(
		cls,
		cur: psycopg.Cursor,
		parent_category_id: int | None,
		name: str,
		created_by: int | None
	) -> ServiceResult:
		norm_name = Utils.normalize_name(name)
		if not Utils.is_valid_name(norm_name):
			return ServiceResult(error=InvalidValueError(Category.ENTITY, Category.COLUMN_NAME))
		
		if created_by is not None and not EPR.has_permission(cur, created_by, PermissionCode.CREATE_CATEGORY):
			return ServiceResult(error=NotAllowedError(PermissionCode.CREATE_CATEGORY, Category.COLUMN_CREATED_BY))
		
		return ServiceResult(
			result=CategoriesRepository.create(
				cur=cur,
				parent_category_id=parent_category_id,
				name=norm_name,
				created_by=created_by
			)
		)
	
	@classmethod
	@BaseService.transaction
	def set_parent_category(
		cls,
		cur: psycopg.Cursor,
		category_id: int,
		parent_category_id: int | None,
		set_by: int | None
	) -> ServiceResult:
		if set_by is not None and not EPR.has_permission(cur, set_by, PermissionCode.SET_CATEGORY_PARENT):
			return ServiceResult(error=NotAllowedError(PermissionCode.SET_CATEGORY_PARENT))
		
		return ServiceResult(
			result=CategoriesRepository.set_parent_category(
				cur=cur,
				category_id=category_id,
				parent_category_id=parent_category_id
			)
		)
		
	@classmethod
	@BaseService.transaction
	def deactivate(
		cls,
		cur: psycopg.Cursor,
		category_id: int,
		deactivated_by: int
	) -> ServiceResult:
		"""
			Errors:
			- NotAllowedError
			- InvalidValueError
			- NotFoundError
			- UnhandledError
		"""
		
		if not EPR.has_permission(cur, deactivated_by, PermissionCode.DEACTIVATE_CATEGORY):
			return ServiceResult(error=NotAllowedError(PermissionCode.DEACTIVATE_CATEGORY, Category.COLUMN_DEACTIVATED_BY))

		if CategoriesRepository.deactivate(cur, category_id, deactivated_by) == UpdateResult.FAIL_NOT_FOUND:
			return ServiceResult(error=NotFoundError(Category.ENTITY, Category.COLUMN_ID))
		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def restore(
		cls,
		cur: psycopg.Cursor,
		category_id: int,
		restored_by: int | None
	) -> ServiceResult:
		"""
			Errors:
			- NotAllowedError
			- NotFoundError
			- UnhandledError
		"""
		
		if restored_by is not None and not EPR.has_permission(cur, restored_by, PermissionCode.CREATE_CATEGORY):
			return ServiceResult(error=NotAllowedError(PermissionCode.CREATE_CATEGORY))

		if CategoriesRepository.restore(cur, category_id) == UpdateResult.FAIL_NOT_FOUND:
			return ServiceResult(error=NotFoundError(Category.ENTITY, Category.COLUMN_ID))
		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def get_by_id(
		cls,
		cur: psycopg.Cursor,
		category_id: int
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- UnhandledError
		"""

		category = CategoriesRepository.get_by_id(cur, category_id)
		if not category:
			return ServiceResult(error=NotFoundError(Category.ENTITY, Category.COLUMN_ID))
		return ServiceResult(result=category)
	
	@classmethod
	@BaseService.transaction
	def get_by_name(
		cls,
		cur: psycopg.Cursor,
		name: str
	) -> ServiceResult:
		"""
			Errors:
			- InvalidValueError
			- NotFoundError
			- UnhandledError
		"""

		norm_name = Utils.normalize_name(name)
		if not Utils.is_valid_name(norm_name):
			return ServiceResult(error=InvalidValueError(Category.ENTITY, Category.COLUMN_NAME))

		category = CategoriesRepository.get_by_name(cur, norm_name)
		if not category:
			return ServiceResult(error=NotFoundError(Category.ENTITY, Category.COLUMN_NAME))
		return ServiceResult(result=category)
	
	@classmethod
	@BaseService.transaction
	def search(
		cls,
		cur: psycopg.Cursor,
		search: str | None = None,
		exclude_deactivated: bool = True,
		limit: int = 50,
		offset: int = 0
	) -> ServiceResult:
		"""
			Errors:
			- UnhandledError
		"""

		return ServiceResult(
			result=CategoriesRepository.search(
				cur=cur,
				search=search,
				exclude_deactivated=exclude_deactivated,
				limit=limit,
				offset=offset
			)
		)
