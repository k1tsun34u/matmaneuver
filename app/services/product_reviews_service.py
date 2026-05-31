import psycopg
from app.types.delete_result import DeleteResult
from app.services.base_service import BaseService
from app.types.service_result import ServiceResult
from app.types.permission_code import PermissionCode
from app.errors.not_found_error import NotFoundError
from app.errors.not_allowed_error import NotAllowedError
from app.types.transaction_helper import TransactionHelper
from app.models.public.product_review import ProductReview
from app.repositories.public.product_reviews_repository import ProductReviewsRepository
from app.repositories.public.employee_permissions_repository import EmployeePermissionsRepository as EPR


class ProductReviewsService(BaseService):
	KEY_HELPERS = tuple()
	FKEY_HELPERS = (TransactionHelper(ProductReview.ENTITY, ProductReview.TABLE, (
		ProductReview.COLUMN_PRODUCT_ID,
		ProductReview.COLUMN_USER_ID,
	)),)

	@classmethod
	@BaseService.transaction
	def create(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		user_id: int,
		rating: int,
		comment: str | None
	) -> ServiceResult:
		"""
			Errors:
			- AlreadyExistsError
			- NotFoundError
			- UnhandledError
		"""

		ProductReviewsRepository.create(
			cur=cur,
			product_id=product_id,
			user_id=user_id,
			rating=rating,
			comment=comment
		)

		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def delete(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		user_id: int,
		deleted_by: int | None
	) -> ServiceResult:
		"""
			Args:
				deleted_by (int | None): employees(id)
			Errors:
			- NotAllowedError
			- NotFoundError
			- UnhandledError
		"""

		if deleted_by is not None and not EPR.has_permission(cur, deleted_by, PermissionCode.DELETE_PRODUCT_REVIEW):
			return ServiceResult(error=NotAllowedError(PermissionCode.DELETE_PRODUCT_REVIEW))

		if ProductReviewsRepository.delete(cur, product_id, user_id) == DeleteResult.FAIL_NOT_FOUND:
			return ServiceResult(error=NotFoundError(ProductReview.ENTITY, ProductReview.COLUMN_PRODUCT_ID))
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
			Args:
				deleted_by (int | None): employees(id)
			Errors:
			- NotAllowedError
			- NotFoundError
			- UnhandledError
		"""

		if deleted_by is not None and not EPR.has_permission(cur, deleted_by, PermissionCode.DELETE_PRODUCT_REVIEW):
			return ServiceResult(error=NotAllowedError(PermissionCode.DELETE_PRODUCT_REVIEW))

		if ProductReviewsRepository.delete_many_by_product_id(cur, product_id) == DeleteResult.FAIL_NOT_FOUND:
			return ServiceResult(error=NotFoundError(ProductReview.ENTITY, ProductReview.COLUMN_PRODUCT_ID))
		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def delete_many_by_user_id(
		cls,
		cur: psycopg.Cursor,
		user_id: int,
		deleted_by: int | None
	) -> ServiceResult:
		"""
			Args:
				deleted_by (int | None): employees(id)
			Errors:
			- NotAllowedError
			- NotFoundError
			- UnhandledError
		"""

		if deleted_by is not None and not EPR.has_permission(cur, deleted_by, PermissionCode.DELETE_PRODUCT_REVIEW):
			return ServiceResult(error=NotAllowedError(PermissionCode.DELETE_PRODUCT_REVIEW))
		
		if ProductReviewsRepository.delete_many_by_user_id(cur, user_id) == DeleteResult.FAIL_NOT_FOUND:
			return ServiceResult(error=NotFoundError(ProductReview.ENTITY, ProductReview.COLUMN_USER_ID))
		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def get_by_product_id_user_id(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		user_id: int
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- UnhandledError
		"""

		product_review = ProductReviewsRepository.get_by_product_id_user_id(cur, product_id, user_id)
		if product_review is None:
			return ServiceResult(error=NotFoundError(ProductReview.ENTITY, ProductReview.COLUMN_PRODUCT_ID))
		return ServiceResult(result=product_review)
	
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
			result=ProductReviewsRepository.get_many_by_product_id(
				cur=cur,
				product_id=product_id,
				limit=limit,
				offset=offset
			)
		)
	
	@classmethod
	@BaseService.transaction
	def get_many_by_user_id(
		cls,
		cur: psycopg.Cursor,
		user_id: int,
		limit: int = 50,
		offset: int = 0
	) -> ServiceResult:
		"""
			Errors:
			- UnhandledError
		"""

		return ServiceResult(
			result=ProductReviewsRepository.get_many_by_user_id(
				cur=cur,
				user_id=user_id,
				limit=limit,
				offset=offset
			)
		)
	
	@classmethod
	@BaseService.transaction
	def get_average_product_rating(
		cls,
		cur: psycopg.Cursor,
		product_id: int
	) -> ServiceResult:
		"""
			Errors:
			- UnhandledError
		"""

		return ServiceResult(
			result=ProductReviewsRepository.get_average_product_rating(cur, product_id)
		)
