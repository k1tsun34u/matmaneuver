import psycopg
from typing import ClassVar
from app.types.order_status import OrderStatus
from app.repositories.base.base_repository import BaseRepository
from app.models.public.order_status_history import OrderStatusHistory
from app.repositories.base.mixins.selectable_mixin import SelectableMixin


class OrderStatusHistoryRepository(
	BaseRepository,
	SelectableMixin[OrderStatusHistory]
):
	TABLE: ClassVar[str] = OrderStatusHistory.TABLE
	MODEL = OrderStatusHistory
	TABLE_COLUMNS = (
		OrderStatusHistory.COLUMN_ID,
		OrderStatusHistory.COLUMN_ORDER_ID,
		OrderStatusHistory.COLUMN_STATUS,
		OrderStatusHistory.COLUMN_CHANGED_BY,
		OrderStatusHistory.COLUMN_CHANGED_AT,
	)

	# warning: get_latest_by_product_id uses this class var!
	ORDER_BY = (
		(OrderStatusHistory.COLUMN_CHANGED_AT, "DESC",),
		(OrderStatusHistory.COLUMN_ID, "DESC",),
	)

	@classmethod
	def create(
		cls,
		cur: psycopg.Cursor,
		order_id: int,
		status: OrderStatus,
		changed_by: int | None
	) -> int:
		return cls.execute_create(
			cur=cur,
			table=cls.TABLE,
			fields={
				OrderStatusHistory.COLUMN_ORDER_ID: order_id,
				OrderStatusHistory.COLUMN_STATUS: status,
				OrderStatusHistory.COLUMN_CHANGED_BY: changed_by
			},
			returning=OrderStatusHistory.COLUMN_ID
		)[OrderStatusHistory.COLUMN_ID]
	
	@classmethod
	def get_by_id(cls, cur: psycopg.Cursor, order_status_history_id: int) -> OrderStatusHistory | None:
		return cls.select(cur=cur, equals={OrderStatusHistory.COLUMN_ID: order_status_history_id})
	
	@classmethod
	def get_many_by_order_id(
		cls,
		cur: psycopg.Cursor,
		order_id: int,
		limit: int = 50,
		offset: int = 0,
	) -> list[OrderStatusHistory]:
		return cls.select_many(
			cur=cur,
			equals={OrderStatusHistory.COLUMN_ORDER_ID: order_id},
			limit=limit,
			offset=offset
		)
	
	@classmethod
	def get_latest_by_order_id(
		cls,
		cur: psycopg.Cursor,
		order_id: int
	) -> OrderStatusHistory | None:
		res = cls.select_many(
			cur=cur,
			equals={OrderStatusHistory.COLUMN_ORDER_ID: order_id},
			limit=1,
			offset=0
		)

		return res[0] if res else None
