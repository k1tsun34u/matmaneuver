from typing import ClassVar

import psycopg
from decimal import Decimal
from app.models.public.write_off_item import WriteOffItem
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.selectable_mixin import SelectableMixin


class WriteOffItemsRepository(
	BaseRepository,
	SelectableMixin[WriteOffItem]
):
	TABLE: ClassVar[str] = WriteOffItem.TABLE
	MODEL = WriteOffItem
	TABLE_COLUMNS = (
		WriteOffItem.COLUMN_ID,
		WriteOffItem.COLUMN_WRITE_OFF_ID,
		WriteOffItem.COLUMN_PRODUCT_ID,
		WriteOffItem.COLUMN_QUANTITY,
		WriteOffItem.COLUMN_PRICE,
	)

	ORDER_BY = ((WriteOffItem.COLUMN_ID, "ASC",),)

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
				WriteOffItem.COLUMN_WRITE_OFF_ID: write_off_id,
				WriteOffItem.COLUMN_PRODUCT_ID: product_id,
				WriteOffItem.COLUMN_QUANTITY: quantity,
				WriteOffItem.COLUMN_PRICE: price
			},
			returning=WriteOffItem.COLUMN_ID
		)[WriteOffItem.COLUMN_ID]
	
	@classmethod
	def get_by_id(cls, cur: psycopg.Cursor, write_off_item_id: int) -> WriteOffItem | None:
		return cls.select(cur, {WriteOffItem.COLUMN_ID: write_off_item_id})
	
	@classmethod
	def get_many_by_write_off_id(
		cls,
		cur: psycopg.Cursor,
		write_off_id: int,
		limit: int = 50,
		offset: int = 0
	) -> tuple[list[WriteOffItem], int]:
		items = cls.select_many(
			cur=cur,
			equals={WriteOffItem.COLUMN_WRITE_OFF_ID: write_off_id},
			limit=limit,
			offset=offset
		)

		query = f"""
			SELECT COUNT(*) as total
			FROM {cls.TABLE}
			WHERE {WriteOffItem.COLUMN_WRITE_OFF_ID} = %s
		"""
		cur.execute(query, (write_off_id,))
		return (items, cur.fetchone()['total'],)
	
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
			equals={WriteOffItem.COLUMN_PRODUCT_ID: product_id},
			limit=limit,
			offset=offset
		)
