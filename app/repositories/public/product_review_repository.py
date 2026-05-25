import psycopg
from typing import ClassVar
from app.types.delete_result import DeleteResult
from app.models.public.product_review import ProductReview
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.selectable_mixin import SelectableMixin


class ProductReviewsRepository(
	BaseRepository,
	SelectableMixin[ProductReview]
):
	TABLE: ClassVar[str] = ProductReview.TABLE
	MODEL = ProductReview
	TABLE_COLUMNS = (
		ProductReview.COLUMN_PRODUCT_ID,
		ProductReview.COLUMN_USER_ID,
		ProductReview.COLUMN_RATING,
		ProductReview.COLUMN_COMMENT,
		ProductReview.COLUMN_CREATED_AT,
	)

	ORDER_BY = ((ProductReview.COLUMN_CREATED_AT, "DESC",),)

	@classmethod
	def create(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		user_id: int,
		rating: int,
		comment: str | None
	) -> None:
		cls.execute_create(
			cur=cur,
			table=cls.TABLE,
			fields={
				ProductReview.COLUMN_PRODUCT_ID: product_id,
				ProductReview.COLUMN_USER_ID: user_id,
				ProductReview.COLUMN_RATING: rating,
				ProductReview.COLUMN_COMMENT: comment
			},
			returning=None
		)
	
	@classmethod
	def delete(cls, cur: psycopg.Cursor, product_id: int, user_id: int) -> DeleteResult:
		rowcount = cls.execute_delete(
			cur=cur,
			table=cls.TABLE,
			where={
				ProductReview.COLUMN_PRODUCT_ID: product_id,
				ProductReview.COLUMN_USER_ID: user_id
			}
		)

		if rowcount != 0:
			return DeleteResult.SUCCESS
		return DeleteResult.FAIL_NOT_FOUND
	
	@classmethod
	def delete_many_by_product_id(
		cls,
		cur: psycopg.Cursor,
		product_id: int
	) -> DeleteResult:
		rowcount = cls.execute_delete(
			cur=cur,
			table=cls.TABLE,
			where={ProductReview.COLUMN_PRODUCT_ID: product_id}
		)

		if rowcount != 0:
			return DeleteResult.SUCCESS
		
		# product may not have any reviews
		return DeleteResult.SUCCESS
	
	@classmethod
	def delete_many_by_user_id(
		cls,
		cur: psycopg.Cursor,
		user_id: int
	) -> DeleteResult:
		rowcount = cls.execute_delete(
			cur=cur,
			table=cls.TABLE,
			where={ProductReview.COLUMN_USER_ID: user_id}
		)

		if rowcount != 0:
			return DeleteResult.SUCCESS
		
		# user may not have any reviews
		return DeleteResult.SUCCESS

	@classmethod
	def get_by_product_id_user_id(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		user_id: int
	) -> ProductReview | None:
		return cls.select(cur, {ProductReview.COLUMN_PRODUCT_ID: product_id, ProductReview.COLUMN_USER_ID: user_id})
	
	@classmethod
	def get_many_by_product_id(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		limit: int = 50,
		offset: int = 0
	) -> list[ProductReview]:
		return cls.select_many(
			cur=cur,
			equals={ProductReview.COLUMN_PRODUCT_ID: product_id},
			limit=limit,
			offset=offset
		)
