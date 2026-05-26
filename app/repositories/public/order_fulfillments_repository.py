import psycopg
from typing import ClassVar
from app.models.public.order_fulfillment import OrderFulfillment
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.selectable_mixin import SelectableMixin


class OrderFulfillmentsRepository(
	BaseRepository,
	SelectableMixin[OrderFulfillment]
):
	TABLE: ClassVar[str] = OrderFulfillment.TABLE
	MODEL = OrderFulfillment
	TABLE_COLUMNS = (
		OrderFulfillment.COLUMN_ID,
		OrderFulfillment.COLUMN_ORDER_ID,
		OrderFulfillment.COLUMN_WAREHOUSE_ID,
		OrderFulfillment.COLUMN_CREATED_AT,
	)

	ORDER_BY = ((OrderFulfillment.COLUMN_CREATED_AT, "DESC",),)

	@classmethod
	def create(
		cls,
		cur: psycopg.Cursor,
		order_id: int,
		warehouse_id: int
	) -> int:
		return cls.execute_create(
			cur=cur,
			table=cls.TABLE,
			fields={
				OrderFulfillment.COLUMN_ORDER_ID: order_id,
				OrderFulfillment.COLUMN_WAREHOUSE_ID: warehouse_id
			},
			returning=OrderFulfillment.COLUMN_ID
		)[OrderFulfillment.COLUMN_ID]
	
	@classmethod
	def get_by_id(
		cls,
		cur: psycopg.Cursor,
		order_fulfillment_id: int
	) -> OrderFulfillment | None:
		return cls.select(
			cur=cur,
			equals={OrderFulfillment.COLUMN_ID: order_fulfillment_id}
		)
	
	@classmethod
	def get_by_id_for_update(
		cls,
		cur: psycopg.Cursor,
		order_fulfillment_id: int
	) -> OrderFulfillment | None:
		query = f"""
			SELECT {", ".join(cls.TABLE_COLUMNS)}
			FROM {cls.TABLE}
			WHERE {OrderFulfillment.COLUMN_ID} = %s
			FOR UPDATE
			LIMIT 1
		"""
		cur.execute(query, (order_fulfillment_id,))
		row = cur.fetchone()
		return OrderFulfillment(**row) if row else None

	@classmethod
	def get_many_by_order_id(
		cls,
		cur: psycopg.Cursor,
		order_id: int,
		limit: int = 50,
		offset: int = 0
	) -> list[OrderFulfillment]:
		return cls.select_many(
			cur=cur,
			equals={OrderFulfillment.COLUMN_ORDER_ID: order_id},
			limit=limit,
			offset=offset
		)
	
	@classmethod
	def get_many_by_warehouse_id(
		cls,
		cur: psycopg.Cursor,
		warehouse_id: int,
		limit: int = 50,
		offset: int = 0
	) -> list[OrderFulfillment]:
		return cls.select_many(
			cur=cur,
			equals={OrderFulfillment.COLUMN_WAREHOUSE_ID: warehouse_id},
			limit=limit,
			offset=offset
		)
