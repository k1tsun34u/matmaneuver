import psycopg
from app.types.return_status import ReturnStatus
from app.repositories.base.base_repository import BaseRepository
from app.models.public.order_return_status_history import OrderReturnStatusHistory
from app.repositories.base.mixins.selectable_mixin import SelectableMixin


class OrderReturnStatusHistoryRepository(
	BaseRepository,
	SelectableMixin[OrderReturnStatusHistory]
):
	TABLE = "order_return_status_history"
	MODEL = OrderReturnStatusHistory
	TABLE_COLUMNS = (
		"id",
		"order_return_id",
		"status",
		"changed_by",
		"changed_at",
	)

	# warning: get_latest_by_return_id uses this class var!
	ORDER_BY = (("changed_at", "DESC"), ("id", "DESC",),)

	@classmethod
	def create(
		cls,
		cur: psycopg.Cursor,
		order_return_id: int,
		status: ReturnStatus,
		changed_by: int | None
	) -> int:
		return cls.execute_create(
			cur=cur,
			table=cls.TABLE,
			fields={
				"order_return_id": order_return_id,
				"status": status,
				"changed_by": changed_by
			},
			returning="id"
		)["id"]
	
	@classmethod
	def get_by_id(cls, cur: psycopg.Cursor, order_return_status_history_id: int) -> OrderReturnStatusHistory | None:
		return cls.select(cur=cur, equals={"id": order_return_status_history_id})
	
	@classmethod
	def get_many_by_order_return_id(
		cls,
		cur: psycopg.Cursor,
		order_return_id: int,
		limit: int = 50,
		offset: int = 0,
	) -> list[OrderReturnStatusHistory]:
		return cls.select_many(
			cur=cur,
			equals={"order_return_id": order_return_id},
			limit=limit,
			offset=offset
		)
	
	@classmethod
	def get_latest_by_order_return_id(
		cls,
		cur: psycopg.Cursor,
		order_return_id: int
	) -> OrderReturnStatusHistory | None:
		res = cls.select_many(
			cur=cur,
			equals={"order_return_id": order_return_id},
			limit=1,
			offset=0
		)

		return res[0] if res else None
