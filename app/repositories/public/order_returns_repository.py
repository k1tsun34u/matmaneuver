import psycopg
from app.types.return_status import ReturnStatus
from app.models.public.order_return import OrderReturn
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.selectable_mixin import SelectableMixin


class OrderReturnsRepository(
	BaseRepository,
	SelectableMixin[OrderReturn]
):
	TABLE = "order_returns"
	MODEL = OrderReturn
	TABLE_COLUMNS = (
		"id",
		"order_id",
		"reason",
		"current_status",
		"created_by",
		"created_at",
	)

	ORDER_BY = (("created_at", "DESC"),)

	@classmethod
	def create(
		cls,
		cur: psycopg.Cursor,
		order_id: int,
		reason: str,
		created_by: int
	) -> int:
		return cls.execute_create(
			cur=cur,
			table=cls.TABLE,
			fields={
				"order_id": order_id,
				"reason": reason,
				"current_status": ReturnStatus.CREATED,
				"created_by": created_by
			},
			returning="id"
		)["id"]
	
	@classmethod
	def change_status(
		cls,
		cur: psycopg.Cursor,
		order_return_id: int,
		status: ReturnStatus
	) -> bool:
		cls.execute_update(
			cur=cur,
			table=cls.TABLE,
			where={"id": order_return_id},
			fields={"current_status": status}
		)

		cur.execute(f"SELECT 1 FROM {cls.TABLE} WHERE id = %s", (order_return_id,))
		return bool(cur.fetchone())
	
	@classmethod
	def get_by_id(cls, cur: psycopg.Cursor, order_return_id: int) -> OrderReturn | None:
		return cls.select(cur, {"id": order_return_id})
	
	@classmethod
	def get_many_by_order_id(
		cls,
		cur: psycopg.Cursor,
		order_id: int,
		limit: int = 50,
		offset: int = 0
	) -> list[OrderReturn]:
		return cls.select_many(
			cur=cur,
			equals={"order_id": order_id},
			limit=limit,
			offset=offset
		)
