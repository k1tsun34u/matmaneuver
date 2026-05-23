import psycopg
from app.models.public.product_category import ProductCategory
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.selectable_mixin import SelectableMixin


class ProductCategoriesRepository(
	BaseRepository,
	SelectableMixin[ProductCategory]
):
	TABLE = "product_categories"
	MODEL = ProductCategory
	SELECT_FIELDS = (
		"product_id",
		"category_id",
		"assigned_by",
		"assigned_at",
	)

	ORDER_BY = (("assigned_at", "DESC"),)

	@classmethod
	def assign(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		category_id: int,
		assigned_by: int | None
	) -> None:
		cls.execute_create(
			cur=cur,
			table=cls.TABLE,
			fields={
				"product_id": product_id,
				"category_id": category_id,
				"assigned_by": assigned_by
			},
			returning=None
		)
	
	@classmethod
	def unassign(cls, cur: psycopg.Cursor, product_id: int, category_id: int) -> int:
		return cls.execute_delete(cur, cls.TABLE, {
			"product_id": product_id,
			"category_id": category_id
		})
	
	@classmethod
	def assign_many(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		category_ids: tuple[int, ...],
		assigned_by: int | None
	) -> int:
		if not category_ids:
			return 0
		
		category_ids = list(dict.fromkeys(category_ids))
		query = f"""
			INSERT INTO {cls.TABLE} ({", ".join(cls.SELECT_FIELDS)})
			SELECT
				%s,
				unnest(%s::bigint[]),
				%s,
				NOW()
			ON CONFLICT (product_id, category_id) DO NOTHING
		"""
		cur.execute(query, (product_id, category_ids, assigned_by,))
		return cur.rowcount
	
	@classmethod
	def unassign_many(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		category_ids: tuple[int, ...]
	) -> int:
		if not category_ids:
			return 0
		
		category_ids = list(dict.fromkeys(category_ids))
		query = f"""
			DELETE FROM {cls.TABLE} pc
			USING (
				SELECT unnest(%s::bigint[]) AS category_id
			) c
			WHERE pc.product_id = %s AND pc.category_id = c.category_id
		"""
		cur.execute(query, (category_ids, product_id,))
		return cur.rowcount
	
	@classmethod
	def get_by_product_id_category_id(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		category_id: int
	) -> ProductCategory | None:
		return cls.select(cur, {"product_id": product_id, "category_id": category_id})
	
	@classmethod
	def get_many_by_product_id(cls, cur: psycopg.Cursor, product_id: int) -> list[ProductCategory]:
		return cls.select_many(cur, {"product_id": product_id})
	
	@classmethod
	def get_many_by_category_id(cls, cur: psycopg.Cursor, category_id: int) -> list[ProductCategory]:
		return cls.select_many(cur, {"category_id": category_id})