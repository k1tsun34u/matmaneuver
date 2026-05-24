import psycopg
from decimal import Decimal
from app.utils import Utils
from app.models.public.product import Product
from app.types.update_result import UpdateResult
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.selectable_mixin import SelectableMixin
from app.repositories.base.mixins.audit_state_mixin import AuditStateMixin


class ProductsRepository(
	BaseRepository,
	AuditStateMixin,
	SelectableMixin[Product]
):
	TABLE = "products"
	MODEL = Product
	TABLE_COLUMNS = (
		"id",
		"name",
		"description",
		"price",
		"deleted_by",
		"deleted_at",
		"created_by",
		"created_at",
	)

	ORDER_BY = (("created_at", "DESC"),)

	@classmethod
	def create(
		cls,
		cur: psycopg.Cursor,
		name: str,
		description: str | None,
		price: Decimal,
		created_by: int | None
	) -> int:
		return cls.execute_create(
			cur=cur,
			table=cls.TABLE,
			fields={
				"name": name,
				"description": description,
				"price": price,
				"created_by": created_by
			},
			returning="id"
		)["id"]
	
	@classmethod
	def set_description(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		description: str | None
	) -> bool:
		cls.execute_update(
			cur=cur,
			table=cls.TABLE,
			where={"id": product_id},
			fields={"description": description}
		)

		cur.execute(f"SELECT 1 FROM {cls.TABLE} WHERE id = %s", (product_id,))
		return bool(cur.fetchone())
	
	@classmethod
	def set_price(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		price: Decimal
	) -> bool:
		cls.execute_update(
			cur=cur,
			table=cls.TABLE,
			where={"id": product_id},
			fields={"price": price}
		)

		cur.execute(f"SELECT 1 FROM {cls.TABLE} WHERE id = %s", (product_id,))
		return bool(cur.fetchone())
	
	@classmethod
	def soft_delete(cls, cur: psycopg.Cursor, product_id: int, deleted_by: int) -> UpdateResult:
		return cls.set_state(cur, "deleted", {"id": product_id}, deleted_by)
	
	@classmethod
	def restore(cls, cur: psycopg.Cursor, product_id: int) -> UpdateResult:
		return cls.clear_state(cur, "deleted", {"id": product_id})
	
	@classmethod
	def get_by_id(cls, cur: psycopg.Cursor, product_id: int) -> Product | None:
		return cls.select(cur, {"id": product_id})
	
	@classmethod
	def search(
		cls,
		cur: psycopg.Cursor,
		search: str | None = None,
		min_price: Decimal | None = None,
		max_price: Decimal | None = None,
		exclude_deleted: bool = True,
		limit: int = 50,
		offset: int = 0
	) -> list[Product]:
		limit, offset = Utils.normalize_pagination(limit, offset)
		conditions = []
		params = []
		if exclude_deleted:
			conditions.append("deleted_at IS NULL")
		if search:
			conditions.append("(name ILIKE %s OR description ILIKE %s)")
			pattern = f"%{search}%"
			params.extend([pattern, pattern])
		if min_price is not None:
			conditions.append("price >= %s")
			params.append(min_price)
		if max_price is not None:
			conditions.append("price <= %s")
			params.append(max_price)

		query = f"""
			SELECT {", ".join(cls.TABLE_COLUMNS)}
			FROM {cls.TABLE}
			{Utils.build_where(tuple(conditions))}
			{Utils.build_order_by(cls.ORDER_BY)}
			LIMIT %s
			OFFSET %s
		"""
		cur.execute(query, (*params, limit, offset))
		return [cls.MODEL(**row) for row in cur.fetchall()]