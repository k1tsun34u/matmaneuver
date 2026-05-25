import psycopg
from app.utils import Utils
from app.models.public.product import Product
from app.types.delete_result import DeleteResult
from app.services.base_service import BaseService
from app.types.service_result import ServiceResult
from app.types.permission_code import PermissionCode
from app.errors.not_found_error import NotFoundError
from app.models.public.product_image import ProductImage
from app.errors.not_allowed_error import NotAllowedError
from app.types.transaction_helper import TransactionHelper
from app.errors.invalid_value_error import InvalidValueError
from app.repositories.public.product_images_repository import ProductImagesRepository
from app.repositories.public.employee_permissions_repository import EmployeePermissionsRepository as EPR


class ProductImagesService(BaseService):
	KEY_HELPERS = (TransactionHelper(ProductImage.ENTITY, ProductImage.TABLE, (ProductImage.COLUMN_STORAGE_KEY,)),)
	FKEY_HELPERS = (TransactionHelper(ProductImage.ENTITY, ProductImage.TABLE, (
		ProductImage.COLUMN_PRODUCT_ID,
		ProductImage.COLUMN_CREATED_BY,
	)),)

	@classmethod
	@BaseService.transaction
	def create(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		storage_key: str,
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

		norm_storage_key = Utils.normalize_storage_key(storage_key)
		if not Utils.is_valid_storage_key(norm_storage_key):
			return ServiceResult(error=InvalidValueError(ProductImage.ENTITY, ProductImage.COLUMN_STORAGE_KEY))

		if created_by is not None and not EPR.has_permission(cur, created_by, PermissionCode.CREATE_PRODUCT_IMAGE):
			return ServiceResult(error=NotAllowedError(PermissionCode.CREATE_PRODUCT_IMAGE, ProductImage.COLUMN_CREATED_BY))

		return ServiceResult(
			result=ProductImagesRepository.create(
				cur=cur,
				product_id=product_id,
				storage_key=norm_storage_key,
				created_by=created_by
			)
		)
	
	@classmethod
	@BaseService.transaction
	def delete(
		cls,
		cur: psycopg.Cursor,
		product_image_id: int,
		deleted_by: int | None
	) -> ServiceResult:
		"""
			Errors:
			- NotAllowedError
			- NotFoundError
			- UnhandledError
		"""

		if deleted_by is not None and not EPR.has_permission(cur, deleted_by, PermissionCode.DELETE_PRODUCT_IMAGE):
			return ServiceResult(error=NotAllowedError(PermissionCode.DELETE_PRODUCT_IMAGE))

		if ProductImagesRepository.delete(cur, product_image_id) == DeleteResult.FAIL_NOT_FOUND:
			return ServiceResult(error=NotFoundError(ProductImage.ENTITY, ProductImage.COLUMN_ID))
		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def delete_many_by_product_id(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		deleted_by: int | None
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- UnhandledError
		"""

		if deleted_by is not None and not EPR.has_permission(cur, deleted_by, PermissionCode.DELETE_PRODUCT_IMAGE):
			return ServiceResult(error=NotAllowedError(PermissionCode.DELETE_PRODUCT_IMAGE))

		ProductImagesRepository.delete_many_by_product_id(cur, product_id)
		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def get_by_id(
		cls,
		cur: psycopg.Cursor,
		product_image_id: int
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- UnhandledError
		"""

		image = ProductImagesRepository.get_by_id(cur, product_image_id)
		if image is None:
			return ServiceResult(error=NotFoundError(ProductImage.ENTITY, ProductImage.COLUMN_ID))
		return ServiceResult(result=image)
	
	@classmethod
	@BaseService.transaction
	def get_by_storage_key(
		cls,
		cur: psycopg.Cursor,
		storage_key: str
	) -> ServiceResult:
		"""
			Errors:
			- InvalidValueError
			- NotFoundError
			- UnhandledError
		"""

		norm_storage_key = Utils.normalize_storage_key(storage_key)
		if not Utils.is_valid_storage_key(norm_storage_key):
			return ServiceResult(error=InvalidValueError(ProductImage.ENTITY, ProductImage.COLUMN_STORAGE_KEY))

		image = ProductImagesRepository.get_by_storage_key(cur, norm_storage_key)
		if image is None:
			return ServiceResult(error=NotFoundError(ProductImage.ENTITY, ProductImage.COLUMN_STORAGE_KEY))
		return ServiceResult(result=image)
	
	@classmethod
	@BaseService.transaction
	def get_many_by_product_id(
		cls,
		cur: psycopg.Cursor,
		product_id: int
	) -> ServiceResult:
		"""
			Errors:
			- UnhandledError
		"""

		return ServiceResult(
			result=ProductImagesRepository.get_many_by_product_id(cur, product_id)
		)
	
	@classmethod
	@BaseService.transaction
	def get_many_by_employee_id(
		cls,
		cur: psycopg.Cursor,
		employee_id: int,
		limit: int = 50,
		offset: int = 0
	) -> ServiceResult:
		"""
			Errors:
			- UnhandledError
		"""

		return ServiceResult(
			result=ProductImagesRepository.get_many_by_employee_id(
				cur=cur,
				employee_id=employee_id,
				limit=limit,
				offset=offset
			)
		)
