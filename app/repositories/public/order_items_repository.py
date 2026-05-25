import psycopg
from decimal import Decimal
from typing import ClassVar
from app.models.public.product import Product
from app.types.delete_result import DeleteResult
from app.models.public.order_item import OrderItem
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.selectable_mixin import SelectableMixin


class OrderItemsRepository(
	BaseRepository,
	SelectableMixin[OrderItem]
):
	TABLE: ClassVar[str] = OrderItem.TABLE
	MODEL = OrderItem
	TABLE_COLUMNS = (
		OrderItem.COLUMN_ID,
		OrderItem.COLUMN_ORDER_ID,
		OrderItem.COLUMN_PRODUCT_ID,
		OrderItem.COLUMN_QUANTITY,
		OrderItem.COLUMN_PRICE,
	)

	ORDER_BY = ((OrderItem.COLUMN_ID, "ASC",),)

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
				OrderItem.COLUMN_ORDER_ID: order_id,
				OrderItem.COLUMN_PRODUCT_ID: product_id,
				OrderItem.COLUMN_QUANTITY: quantity,
				OrderItem.COLUMN_PRICE: price
			},
			returning=OrderItem.COLUMN_ID
		)[OrderItem.COLUMN_ID]
	
	@classmethod
	def delete(
		cls,
		cur: psycopg.Cursor,
		order_item_id: int
	) -> DeleteResult:
		rowcount = cls.execute_delete(
			cur=cur,
			table=cls.TABLE,
			where={OrderItem.COLUMN_ID: order_item_id}
		)

		if rowcount != 0:
			return DeleteResult.SUCCESS
		return DeleteResult.FAIL_NOT_FOUND
	
	@classmethod
	def get_by_id(cls, cur: psycopg.Cursor, order_item_id: int) -> OrderItem | None:
		return cls.select(cur, {OrderItem.COLUMN_ID: order_item_id})
	
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
			equals={OrderItem.COLUMN_ORDER_ID: order_id},
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
			equals={OrderItem.COLUMN_PRODUCT_ID: product_id},
			limit=limit,
			offset=offset
		)
