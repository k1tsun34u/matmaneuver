import psycopg
from app.models.public.product_review import ProductReview
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.selectable_mixin import SelectableMixin


class ProductReviewsRepository(
	BaseRepository,
	SelectableMixin[ProductReview]
):
	TABLE = "product_reviews"
	MODEL = ProductReview
	TABLE_COLUMNS = (
		"product_id",
		"user_id",
		"rating",
		"comment",
		"created_at",
	)

	ORDER_BY = (("created_at", "DESC"),)

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
				"product_id": product_id,
				"user_id": user_id,
				"rating": rating,
				"comment": comment
			},
			returning=None
		)
	
	@classmethod
	def delete(cls, cur: psycopg.Cursor, product_id: int, user_id: int) -> int:
		return cls.execute_delete(cur, cls.TABLE, {"product_id": product_id, "user_id": user_id})
	
	@classmethod
	def delete_many_by_product_id(
		cls,
		cur: psycopg.Cursor,
		product_id: int
	) -> int:
		return cls.execute_delete(
			cur=cur,
			table=cls.TABLE,
			where={"product_id": product_id}
		)
	
	@classmethod
	def delete_many_by_user_id(
		cls,
		cur: psycopg.Cursor,
		user_id: int
	) -> int:
		return cls.execute_delete(
			cur=cur,
			table=cls.TABLE,
			where={"user_id": user_id}
		)

	@classmethod
	def get_by_product_id_user_id(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		user_id: int
	) -> ProductReview | None:
		return cls.select(cur, {"product_id": product_id, "user_id": user_id})
	
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
			equals={"product_id": product_id},
			limit=limit,
			offset=offset
		)
