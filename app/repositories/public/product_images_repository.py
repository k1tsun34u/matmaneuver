import psycopg
from app.models.public.product_image import ProductImage
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.selectable_mixin import SelectableMixin


class ProductImagesRepository(
	BaseRepository,
	SelectableMixin[ProductImage]
):
	TABLE = "product_images"
	MODEL = ProductImage
	SELECT_FIELDS = (
		"id",
		"product_id",
		"storage_key",
		"created_by",
		"created_at",
	)

	ORDER_BY = (("created_at", "DESC"),)

	@classmethod
	def create(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		storage_key: str,
		created_by: int | None
	) -> int:
		return cls.execute_create(
			cur=cur,
			table=cls.TABLE,
			fields={
				"product_id": product_id,
				"storage_key": storage_key,
				"created_by": created_by
			},
			returning="id"
		)["id"]
	
	@classmethod
	def delete(cls, cur: psycopg.Cursor, product_image_id: int) -> int:
		return cls.execute_delete(cur, cls.TABLE, {"id": product_image_id})
	
	@classmethod
	def delete_many_by_product_id(cls, cur: psycopg.Cursor, product_id: int) -> int:
		query = f"""
			DELETE FROM {cls.TABLE}
			WHERE product_id = %s
		"""
		cur.execute(query, (product_id,))
		return cur.rowcount

	@classmethod
	def get_by_id(cls, cur: psycopg.Cursor, product_image_id: int) -> ProductImage | None:
		return cls.select(cur, {"id": product_image_id})
	
	@classmethod
	def get_many_by_product_id(cls, cur: psycopg.Cursor, product_id: int) -> list[ProductImage]:
		return cls.select_many(cur, {"product_id": product_id})