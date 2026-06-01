import psycopg
from typing import ClassVar
from app.types.delete_result import DeleteResult
from app.models.public.product_image import ProductImage
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.selectable_mixin import SelectableMixin


class ProductImagesRepository(
	BaseRepository,
	SelectableMixin[ProductImage]
):
	TABLE: ClassVar[str] = ProductImage.TABLE
	MODEL = ProductImage
	TABLE_COLUMNS = (
		ProductImage.COLUMN_ID,
		ProductImage.COLUMN_PRODUCT_ID,
		ProductImage.COLUMN_STORAGE_KEY,
		ProductImage.COLUMN_CREATED_BY,
		ProductImage.COLUMN_CREATED_AT,
	)

	ORDER_BY = ((ProductImage.COLUMN_ID, "ASC",),)

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
			table=ProductImage.TABLE,
			fields={
				ProductImage.COLUMN_PRODUCT_ID: product_id,
				ProductImage.COLUMN_STORAGE_KEY: storage_key,
				ProductImage.COLUMN_CREATED_BY: created_by
			},
			returning=ProductImage.COLUMN_ID
		)[ProductImage.COLUMN_ID]
	
	@classmethod
	def delete(cls, cur: psycopg.Cursor, product_image_id: int) -> DeleteResult:
		rowcount = cls.execute_delete(
			cur=cur,
			table=ProductImage.TABLE,
			where={ProductImage.COLUMN_ID: product_image_id}
		)
		
		if rowcount != 0:
			return DeleteResult.SUCCESS
		return DeleteResult.FAIL_NOT_FOUND
	
	@classmethod
	def delete_many_by_product_id(cls, cur: psycopg.Cursor, product_id: int) -> DeleteResult:
		rowcount = cls.execute_delete(
			cur=cur,
			table=ProductImage.TABLE,
			where={ProductImage.COLUMN_PRODUCT_ID: product_id}
		)

		if rowcount != 0:
			return DeleteResult.SUCCESS
		
		# product may not have any images
		return DeleteResult.SUCCESS

	@classmethod
	def get_by_id(cls, cur: psycopg.Cursor, product_image_id: int) -> ProductImage | None:
		return cls.select(cur=cur, equals={ProductImage.COLUMN_ID: product_image_id})

	@classmethod
	def get_by_storage_key(cls, cur: psycopg.Cursor, storage_key: str) -> ProductImage | None:
		return cls.select(cur=cur, equals={ProductImage.COLUMN_STORAGE_KEY: storage_key})
	
	@classmethod
	def get_many_by_product_id(cls, cur: psycopg.Cursor, product_id: int) -> list[ProductImage]:
		return cls.select_many(
			cur=cur,
			equals={ProductImage.COLUMN_PRODUCT_ID: product_id}
		)
	
	@classmethod
	def get_many_by_employee_id(
		cls,
		cur: psycopg.Cursor,
		employee_id: int,
		limit: int = 50,
		offset: int = 0
	) -> tuple[list[ProductImage], int]:
		product_images = cls.select_many(
			cur=cur,
			equals={ProductImage.COLUMN_CREATED_BY: employee_id},
			limit=limit,
			offset=offset
		)

		query = f"""
			SELECT COUNT(*) AS total
			FROM {cls.TABLE}
			WHERE {ProductImage.COLUMN_CREATED_BY} = %s
		"""
		cur.execute(query, (employee_id,))
		return (product_images, cur.fetchone()['total'],)
