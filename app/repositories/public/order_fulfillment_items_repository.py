import psycopg
from typing import ClassVar
from decimal import Decimal
from app.models.public.order_fulfillment import OrderFulfillment
from app.repositories.base.base_repository import BaseRepository
from app.models.public.order_fulfillment_item import OrderFulfillmentItem
from app.repositories.base.mixins.selectable_mixin import SelectableMixin


class OrderFulfillmentItemsRepository(
	BaseRepository,
	SelectableMixin[OrderFulfillmentItem]
):
	TABLE: ClassVar[str] = OrderFulfillmentItem.TABLE
	MODEL = OrderFulfillmentItem
	TABLE_COLUMNS = (
		OrderFulfillmentItem.COLUMN_ID,
		OrderFulfillmentItem.COLUMN_ORDER_FULFILLMENT_ID,
		OrderFulfillmentItem.COLUMN_PRODUCT_ID,
		OrderFulfillmentItem.COLUMN_QUANTITY,
		OrderFulfillmentItem.COLUMN_PRICE,
	)

	ORDER_BY = ((OrderFulfillmentItem.COLUMN_ID, "ASC",),)

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
				OrderFulfillmentItem.COLUMN_ORDER_FULFILLMENT_ID: order_fulfillment_id,
				OrderFulfillmentItem.COLUMN_PRODUCT_ID: product_id,
				OrderFulfillmentItem.COLUMN_QUANTITY: quantity,
				OrderFulfillmentItem.COLUMN_PRICE: price
			},
			returning=OrderFulfillmentItem.COLUMN_ID
		)[OrderFulfillmentItem.COLUMN_ID]
	
	@classmethod
	def get_by_id(cls, cur: psycopg.Cursor, order_fulfillment_item_id: int) -> OrderFulfillmentItem | None:
		return cls.select(
			cur=cur,
			equals={OrderFulfillmentItem.COLUMN_ID: order_fulfillment_item_id}
		)
	
	@classmethod
	def get_many_by_order_fulfillment_id(
		cls,
		cur: psycopg.Cursor,
		order_fulfillment_id: int,
		limit: int = 50,
		offset: int = 0
	) -> tuple[list[OrderFulfillmentItem], int]:
		items = cls.select_many(
			cur=cur,
			equals={OrderFulfillmentItem.COLUMN_ORDER_FULFILLMENT_ID: order_fulfillment_id},
			limit=limit,
			offset=offset
		)

		query = f"""
			SELECT COUNT(*) AS total
			FROM {cls.TABLE}
			WHERE {OrderFulfillmentItem.COLUMN_ORDER_FULFILLMENT_ID} = %s
		"""
		cur.execute(query, (order_fulfillment_id,))
		return (items, cur.fetchone()['total'],)
	
	@classmethod
	def get_many_by_product_id(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		limit: int = 50,
		offset: int = 0
	) -> tuple[list[OrderFulfillmentItem], int]:
		items = cls.select_many(
			cur=cur,
			equals={OrderFulfillmentItem.COLUMN_PRODUCT_ID: product_id},
			limit=limit,
			offset=offset
		)

		query = f"""
			SELECT COUNT(*) AS total
			FROM {cls.TABLE}
			WHERE {OrderFulfillmentItem.COLUMN_PRODUCT_ID} = %s
		"""
		cur.execute(query, (product_id,))
		return (items, cur.fetchone()['total'],)
	
	@classmethod
	def get_total_fulfilled_quantity(
		cls,
		cur: psycopg.Cursor,
		order_id: int,
		product_id: int
	) -> int:
		query = f"""
			SELECT COALESCE(
				SUM(ofi.{OrderFulfillmentItem.COLUMN_QUANTITY}),
					0
			) AS total
			FROM {OrderFulfillmentItem.TABLE} ofi
			JOIN
				{OrderFulfillment.TABLE} fulf
				ON fulf.{OrderFulfillment.COLUMN_ID} = ofi.{OrderFulfillmentItem.COLUMN_ORDER_FULFILLMENT_ID}
			WHERE
				fulf.{OrderFulfillment.COLUMN_ORDER_ID} = %s
				AND ofi.{OrderFulfillmentItem.COLUMN_PRODUCT_ID} = %s
		"""
		cur.execute(query, (order_id, product_id,))
		row = cur.fetchone()
		return row["total"]
