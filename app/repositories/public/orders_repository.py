import psycopg
from app.models.public.order import Order
from app.types.order_status import OrderStatus
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.selectable_mixin import SelectableMixin


class OrdersRepository(
	BaseRepository,
	SelectableMixin[Order]
):
	TABLE = "orders"
	MODEL = Order
	SELECT_FIELDS = (
		"id",
		"current_status",
		"track_number",
		"delivery_address",
		"created_by",
		"created_at",
	)

	ORDER_BY = (("created_at", "DESC"),)

	@classmethod
	def create(
		cls,
		cur: psycopg.Cursor,
		track_number: str,
		delivery_address: str,
		created_by: int
	) -> int:
		return cls.execute_create(
			cur=cur,
			table=cls.TABLE,
			fields={
				"current_status": OrderStatus.CREATED,
				"track_number": track_number,
				"delivery_address": delivery_address,
				"created_by": created_by
			},
			returning="id"
		)["id"]
	
	@classmethod
	def change_status(
		cls,
		cur: psycopg.Cursor,
		order_id: int,
		status: OrderStatus
	) -> int:
		return cls.execute_update(
			cur=cur,
			table=cls.TABLE,
			where={"id": order_id},
			fields={"current_status": status}
		)
	
	@classmethod
	def get_by_id(cls, cur: psycopg.Cursor, order_id: int) -> Order | None:
		return cls.select(cur, {"id": order_id})
	
	@classmethod
	def get_by_track_number(cls, cur: psycopg.Cursor, track_number: str) -> Order | None:
		return cls.select(cur, {"track_number": track_number})
