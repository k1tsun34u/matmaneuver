import psycopg
from typing import ClassVar
from decimal import Decimal
from app.utils import Utils
from app.models.public.product import Product
from app.types.update_result import UpdateResult
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.updatable_mixin import UpdatableMixin
from app.repositories.base.mixins.selectable_mixin import SelectableMixin
from app.repositories.base.mixins.audit_state_mixin import AuditStateMixin


class ProductsRepository(
	BaseRepository,
	AuditStateMixin,
	UpdatableMixin,
	SelectableMixin[Product]
):
	TABLE: ClassVar[str] = Product.TABLE
	MODEL = Product
	TABLE_COLUMNS = (
		Product.COLUMN_ID,
		Product.COLUMN_NAME,
		Product.COLUMN_DESCRIPTION,
		Product.COLUMN_PRICE,
		Product.COLUMN_DELETED_BY,
		Product.COLUMN_DELETED_AT,
		Product.COLUMN_CREATED_BY,
		Product.COLUMN_CREATED_AT,
	)

	ORDER_BY = ((Product.COLUMN_CREATED_AT, "DESC",),)

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
				Product.COLUMN_NAME: name,
				Product.COLUMN_DESCRIPTION: description,
				Product.COLUMN_PRICE: price,
				Product.COLUMN_CREATED_BY: created_by
			},
			returning=Product.COLUMN_ID
		)[Product.COLUMN_ID]
	
	@classmethod
	def set_description(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		description: str | None
	) -> UpdateResult:
		return cls.update_by_conditions(
			cur=cur,
			identity_where={Product.COLUMN_ID: product_id},
			condition_where={},
			fields={Product.COLUMN_DESCRIPTION: description}
		)
	
	@classmethod
	def set_price(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		price: Decimal
	) -> UpdateResult:
		return cls.update_by_conditions(
			cur=cur,
			identity_where={Product.COLUMN_ID: product_id},
			condition_where={},
			fields={Product.COLUMN_PRICE: price}
		)
	
	@classmethod
	def soft_delete(cls, cur: psycopg.Cursor, product_id: int, deleted_by: int | None) -> UpdateResult:
		return cls.set_state(cur, "deleted", {Product.COLUMN_ID: product_id}, deleted_by)
	
	@classmethod
	def restore(cls, cur: psycopg.Cursor, product_id: int) -> UpdateResult:
		return cls.clear_state(cur, "deleted", {Product.COLUMN_ID: product_id})
	
	@classmethod
	def get_by_id(cls, cur: psycopg.Cursor, product_id: int) -> Product | None:
		return cls.select(
			cur=cur,
			equals={Product.COLUMN_ID: product_id}
		)
	
	@classmethod
	def get_many_by_employee_id(
		cls,
		cur: psycopg.Cursor,
		employee_id: int,
		exclude_deleted: bool = True,
		limit: int = 50,
		offset: int = 0
	) -> list[Product]:
		return cls.select_many(
			cur=cur,
			equals={Product.COLUMN_CREATED_BY: employee_id},
			is_null=(Product.COLUMN_DELETED_AT,) if exclude_deleted else None,
			limit=limit,
			offset=offset
		)
	
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
			conditions.append(f"{Product.COLUMN_DELETED_AT} IS NULL")
		if search:
			conditions.append(f"({Product.COLUMN_NAME} ILIKE %s OR {Product.COLUMN_DESCRIPTION} ILIKE %s)")
			pattern = f"%{search}%"
			params.extend([pattern, pattern])
		if min_price is not None:
			conditions.append(f"{Product.COLUMN_PRICE} >= %s")
			params.append(min_price)
		if max_price is not None:
			conditions.append(f"{Product.COLUMN_PRICE} <= %s")
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
