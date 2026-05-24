import psycopg
from decimal import Decimal
from app.models.public.order_item import OrderItem
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.selectable_mixin import SelectableMixin


class OrderItemsRepository(
	BaseRepository,
	SelectableMixin[OrderItem]
):
	TABLE = "order_items"
	MODEL = OrderItem
	TABLE_COLUMNS = (
		"id",
		"order_id",
		"product_id",
		"quantity",
		"price",
	)

	ORDER_BY = (("id", "ASC"),)

	@classmethod
	def create(
		cls,
		cur: psycopg.Cursor,
		order_id: int,
		product_id: int,
		quantity: int,
		price: Decimal
	) -> int:
		return cls.execute_create(
			cur=cur,
			table=cls.TABLE,
			fields={
				"order_id": order_id,
				"product_id": product_id,
				"quantity": quantity,
				"price": price
			},
			returning="id"
		)["id"]
	
	@classmethod
	def get_by_id(cls, cur: psycopg.Cursor, order_item_id: int) -> OrderItem | None:
		return cls.select(cur, {"id": order_item_id})
	
	@classmethod
	def get_many_by_order_id(
		cls,
		cur: psycopg.Cursor,
		order_id: int,
		limit: int = 50,
		offset: int = 0
	) -> list[OrderItem]:
		return cls.select_many(
			cur=cur,
			equals={"order_id": order_id},
			limit=limit,
			offset=offset
		)
	
	@classmethod
	def get_many_by_product_id(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		limit: int = 50,
		offset: int = 0
	) -> list[OrderItem]:
		return cls.select_many(
			cur=cur,
			equals={"product_id": product_id},
			limit=limit,
			offset=offset
		)
