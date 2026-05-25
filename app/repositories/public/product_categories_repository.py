import psycopg
from typing import ClassVar
from collections.abc import Sequence
from app.models.public.product import Product
from app.models.public.category import Category
from app.models.public.product_category import ProductCategory
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.relation_mixin import RelationMixin
from app.repositories.base.mixins.selectable_mixin import SelectableMixin
from app.utils import Utils


class ProductCategoriesRepository(
	BaseRepository,
	RelationMixin,
	SelectableMixin[ProductCategory]
):
	TABLE: ClassVar[str] = ProductCategory.TABLE
	MODEL = ProductCategory
	TABLE_COLUMNS = (
		ProductCategory.COLUMN_PRODUCT_ID,
		ProductCategory.COLUMN_CATEGORY_ID,
		ProductCategory.COLUMN_ASSIGNED_BY,
		ProductCategory.COLUMN_ASSIGNED_AT,
	)

	ORDER_BY = ((ProductCategory.COLUMN_ASSIGNED_AT, "DESC",),)

	@classmethod
	def assign(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		category_id: int,
		assigned_by: int | None
	) -> None:
		return cls.assign_many(
			cur=cur,
			product_id=product_id,
			category_ids=(category_id,),
			assigned_by=assigned_by
		)
	
	@classmethod
	def unassign(cls, cur: psycopg.Cursor, product_id: int, category_id: int) -> None:
		return cls.unassign_many(
			cur=cur,
			product_id=product_id,
			category_ids=(category_id,)
		)
	
	@classmethod
	def assign_many(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		category_ids: Sequence[int],
		assigned_by: int | None
	) -> None:
		cls.create_relations(
			cur=cur,
			fixed_field=ProductCategory.COLUMN_PRODUCT_ID,
			fixed_value=product_id,
			varying_field=ProductCategory.COLUMN_CATEGORY_ID,
			varying_values=category_ids,
			actor_id=assigned_by
		)
	
	@classmethod
	def unassign_many(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		category_ids: Sequence[int]
	) -> None:
		cls.delete_relations(
			cur=cur,
			fixed_field=ProductCategory.COLUMN_PRODUCT_ID,
			fixed_value=product_id,
			varying_field=ProductCategory.COLUMN_CATEGORY_ID,
			varying_values=category_ids
		)
	
	@classmethod
	def get_by_product_id_category_id(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		category_id: int
	) -> ProductCategory | None:
		return cls.select(
			cur=cur,
			equals={
				ProductCategory.COLUMN_PRODUCT_ID: product_id,
				ProductCategory.COLUMN_CATEGORY_ID: category_id
			}
		)
	
	@classmethod
	def get_many_by_product_id(cls, cur: psycopg.Cursor, product_id: int) -> list[ProductCategory]:
		return cls.select_many(
			cur=cur,
			equals={ProductCategory.COLUMN_PRODUCT_ID: product_id}
		)
	
	@classmethod
	def get_many_by_category_id(
		cls,
		cur: psycopg.Cursor,
		category_id: int,
		limit: int = 50,
		offset: int = 0
	) -> list[ProductCategory]:
		return cls.select_many(
			cur=cur,
			equals={ProductCategory.COLUMN_CATEGORY_ID: category_id},
			limit=limit,
			offset=offset
		)
	
	@classmethod
	def get_categories_by_product_id(
		cls,
		cur: psycopg.Cursor,
		product_id: int
	) -> list[Category]:
		query = f"""
			SELECT DISTINCT c.*
			FROM {Category.TABLE} c
			JOIN product_categories pc ON pc.{ProductCategory.COLUMN_CATEGORY_ID} = c.{Category.COLUMN_ID}
			WHERE
				pc.{ProductCategory.COLUMN_PRODUCT_ID} = %s
				AND c.{Category.COLUMN_DEACTIVATED_AT} IS NULL
			{Utils.build_order_by(((Category.COLUMN_CREATED_AT, "DESC",),))}
		"""
		cur.execute(query, (product_id,))
		return [Category(**row) for row in cur.fetchall()]
	
	@classmethod
	def get_products_by_category_id(
		cls,
		cur: psycopg.Cursor,
		category_id: int,
		limit: int = 50,
		offset: int = 0
	) -> list[Product]:
		query = f"""
			SELECT DISTINCT p.*
			FROM {Product.TABLE} p
			JOIN product_categories pc ON pc.{ProductCategory.COLUMN_PRODUCT_ID} = p.{Product.COLUMN_ID}
			WHERE
				pc.{ProductCategory.COLUMN_CATEGORY_ID} = %s
				AND p.{Product.COLUMN_DELETED_AT} IS NULL
			{Utils.build_order_by(((Product.COLUMN_CREATED_AT, "DESC",),))}
			LIMIT %s
			OFFSET %s
		"""
		cur.execute(query, (category_id, limit, offset,))
		return [Product(**row) for row in cur.fetchall()]
