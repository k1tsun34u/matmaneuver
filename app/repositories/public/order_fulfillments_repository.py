import psycopg
from app.models.public.order_fulfillment import OrderFulfillment
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.selectable_mixin import SelectableMixin


class OrderFulfillmentsRepository(
	BaseRepository,
	SelectableMixin[OrderFulfillment]
):
	TABLE = "order_fulfillments"
	MODEL = OrderFulfillment
	SELECT_FIELDS = (
		"id",
		"order_id",
		"warehouse_id",
		"created_at",
	)

	ORDER_BY = (("created_at", "DESC"),)

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
				"order_id": order_id,
				"warehouse_id": warehouse_id
			},
			returning="id"
		)["id"]
	
	@classmethod
	def get_by_id(
		cls,
		cur: psycopg.Cursor,
		order_fulfillment_id: int
	) -> OrderFulfillment | None:
		return cls.select(cur, {"id": order_fulfillment_id})

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
			equals={"order_id": order_id},
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
			equals={"warehouse_id": warehouse_id},
			limit=limit,
			offset=offset
		)
