import psycopg
from decimal import Decimal
from app.models.public.write_off_item import WriteOffItem
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.selectable_mixin import SelectableMixin


class WriteOffItemsRepository(
	BaseRepository,
	SelectableMixin[WriteOffItem]
):
	TABLE = "write_off_items"
	MODEL = WriteOffItem
	TABLE_COLUMNS = (
		"id",
		"write_off_id",
		"product_id",
		"quantity",
		"price",
	)

	ORDER_BY = (("id", "ASC"),)

	@classmethod
	def create(
		cls,
		cur: psycopg.Cursor,
		write_off_id: int,
		product_id: int,
		quantity: int,
		price: Decimal
	) -> int:
		return cls.execute_create(
			cur=cur,
			table=cls.TABLE,
			fields={
				"write_off_id": write_off_id,
				"product_id": product_id,
				"quantity": quantity,
				"price": price
			},
			returning="id"
		)["id"]
	
	@classmethod
	def get_by_id(cls, cur: psycopg.Cursor, write_off_item_id: int) -> WriteOffItem | None:
		return cls.select(cur, {"id": write_off_item_id})
	
	@classmethod
	def get_many_by_write_off_id(
		cls,
		cur: psycopg.Cursor,
		write_off_id: int,
		limit: int = 50,
		offset: int = 0
	) -> list[WriteOffItem]:
		return cls.select_many(
			cur=cur,
			equals={"write_off_id": write_off_id},
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
	) -> list[WriteOffItem]:
		return cls.select_many(
			cur=cur,
			equals={"product_id": product_id},
			limit=limit,
			offset=offset
		)
