import psycopg
from decimal import Decimal
from app.models.public.order_fulfillment_item import OrderFulfillmentItem
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.selectable_mixin import SelectableMixin


class OrderFulfillmentItemsRepository(
	BaseRepository,
	SelectableMixin[OrderFulfillmentItem]
):
	TABLE = "order_fulfillment_items"
	MODEL = OrderFulfillmentItem
	TABLE_COLUMNS = (
		"id",
		"order_fulfillment_id",
		"product_id",
		"quantity",
		"price",
	)

	ORDER_BY = (("id", "ASC",),)

	@classmethod
	def create(
		cls,
		cur: psycopg.Cursor,
		order_fulfillment_id: int,
		product_id: int,
		quantity: int,
		price: Decimal
	) -> int:
		return cls.execute_create(
			cur=cur,
			table=cls.TABLE,
			fields={
				"order_fulfillment_id": order_fulfillment_id,
				"product_id": product_id,
				"quantity": quantity,
				"price": price
			},
			returning="id"
		)["id"]
	
	@classmethod
	def get_by_id(cls, cur: psycopg.Cursor, order_fulfillment_item_id: int) -> OrderFulfillmentItem | None:
		return cls.select(cur, {"id": order_fulfillment_item_id})
	
	@classmethod
	def get_many_by_order_fulfillment_id(
		cls,
		cur: psycopg.Cursor,
		order_fulfillment_id: int,
		limit: int = 50,
		offset: int = 0
	) -> list[OrderFulfillmentItem]:
		return cls.select_many(
			cur=cur,
			equals={"order_fulfillment_id": order_fulfillment_id},
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
	) -> list[OrderFulfillmentItem]:
		return cls.select_many(
			cur=cur,
			equals={"product_id": product_id},
			limit=limit,
			offset=offset
		)
