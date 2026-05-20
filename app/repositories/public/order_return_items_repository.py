import psycopg
from decimal import Decimal
from app.models.public.order_return_item import OrderReturnItem
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.selectable_mixin import SelectableMixin


class OrderReturnItemsRepository(
	BaseRepository,
	SelectableMixin[OrderReturnItem]
):
	TABLE = "order_return_items"
	MODEL = OrderReturnItem
	SELECT_FIELDS = (
		"id",
		"order_return_id",
		"order_item_id",
		"quantity",
		"price",
	)

	ORDER_BY = (("id", "ASC"),)

	@classmethod
	def create(
		cls,
		cur: psycopg.Cursor,
		order_return_id: int,
		order_item_id: int,
		quantity: int,
		price: Decimal
	) -> int:
		return cls.execute_create(
			cur=cur,
			table=cls.TABLE,
			fields={
				"order_return_id": order_return_id,
				"order_item_id": order_item_id,
				"quantity": quantity,
				"price": price
			},
			returning="id"
		)["id"]
	
	@classmethod
	def get_by_id(cls, cur: psycopg.Cursor, order_return_item_id: int) -> OrderReturnItem | None:
		return cls.select(cur, {"id": order_return_item_id})
	
	@classmethod
	def get_many_by_order_return_id(
		cls,
		cur: psycopg.Cursor,
		order_return_id: int,
		limit: int = 50,
		offset: int = 0
	) -> list[OrderReturnItem]:
		return cls.select_many(
			cur=cur,
			equals={"order_return_id": order_return_id},
			limit=limit,
			offset=offset
		)

	@classmethod
	def get_many_by_order_item_id(
		cls,
		cur: psycopg.Cursor,
		order_item_id: int,
		limit: int = 50,
		offset: int = 0
	) -> list[OrderReturnItem]:
		return cls.select_many(
			cur=cur,
			equals={"order_item_id": order_item_id},
			limit=limit,
			offset=offset
		)
