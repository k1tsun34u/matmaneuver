import psycopg
from app.types.order_status import OrderStatus
from app.repositories.base.base_repository import BaseRepository
from app.models.public.order_status_history import OrderStatusHistory
from app.repositories.base.mixins.selectable_mixin import SelectableMixin


class OrderStatusHistoryRepository(
	BaseRepository,
	SelectableMixin[OrderStatusHistory]
):
	TABLE = "order_status_history"
	MODEL = OrderStatusHistory
	TABLE_COLUMNS = (
		"id",
		"order_id",
		"status",
		"changed_by",
		"changed_at",
	)

	# warning: get_latest_by_product_id uses this class var!
	ORDER_BY = (("changed_at", "DESC"), ("id", "DESC"),)

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
				"order_id": order_id,
				"status": status,
				"changed_by": changed_by
			},
			returning="id"
		)["id"]
	
	@classmethod
	def get_by_id(cls, cur: psycopg.Cursor, order_status_history_id: int) -> OrderStatusHistory | None:
		return cls.select(cur=cur, equals={"id": order_status_history_id})
	
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
			equals={"order_id": order_id},
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
			equals={"order_id": order_id},
			limit=1,
			offset=0
		)

		return res[0] if res else None
