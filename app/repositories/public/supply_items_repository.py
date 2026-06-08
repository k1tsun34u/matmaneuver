import psycopg
from typing import ClassVar
from decimal import Decimal
from app.types.delete_result import DeleteResult
from app.models.public.supply_item import SupplyItem
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.selectable_mixin import SelectableMixin


class SupplyItemsRepository(
	BaseRepository,
	SelectableMixin[SupplyItem]
):
	TABLE: ClassVar[str] = SupplyItem.TABLE
	MODEL = SupplyItem
	TABLE_COLUMNS = (
		SupplyItem.COLUMN_ID,
		SupplyItem.COLUMN_SUPPLY_ID,
		SupplyItem.COLUMN_PRODUCT_ID,
		SupplyItem.COLUMN_QUANTITY,
		SupplyItem.COLUMN_PRICE,
	)

	ORDER_BY = ((SupplyItem.COLUMN_ID, "ASC",),)

	@classmethod
	def create(
		cls,
		cur: psycopg.Cursor,
		supply_id: int,
		product_id: int,
		quantity: int,
		price: Decimal
	) -> int:
		return cls.execute_create(
			cur=cur,
			table=cls.TABLE,
			fields={
				SupplyItem.COLUMN_SUPPLY_ID: supply_id,
				SupplyItem.COLUMN_PRODUCT_ID: product_id,
				SupplyItem.COLUMN_QUANTITY: quantity,
				SupplyItem.COLUMN_PRICE: price
			},
			returning=SupplyItem.COLUMN_ID
		)[SupplyItem.COLUMN_ID]
	
	@classmethod
	def delete(
		cls,
		cur: psycopg.Cursor,
		supply_item_id: int
	) -> DeleteResult:
		rowcount = cls.execute_delete(
			cur=cur,
			table=cls.TABLE,
			where={SupplyItem.COLUMN_ID: supply_item_id}
		)

		if rowcount != 0:
			return DeleteResult.SUCCESS
		return DeleteResult.FAIL_NOT_FOUND
	
	@classmethod
	def get_by_id(cls, cur: psycopg.Cursor, supply_item_id: int) -> SupplyItem | None:
		return cls.select(cur, {SupplyItem.COLUMN_ID: supply_item_id})
	
	@classmethod
	def get_many_by_supply_id(
		cls,
		cur: psycopg.Cursor,
		supply_id: int,
		limit: int = 50,
		offset: int = 0
	) -> tuple[list[SupplyItem], int]:
		items = cls.select_many(
			cur=cur,
			equals={SupplyItem.COLUMN_SUPPLY_ID: supply_id},
			limit=limit,
			offset=offset
		)

		query = f"""
			SELECT COUNT(*) as total
			FROM {cls.TABLE}
			WHERE {SupplyItem.COLUMN_SUPPLY_ID} = %s
		"""
		cur.execute(query, (supply_id,))
		return (items, cur.fetchone()['total'],)
	
	@classmethod
	def get_all_by_supply_id(
		cls,
		cur: psycopg.Cursor,
		supply_id: int
	) -> list[SupplyItem]:
		query = f"""
			SELECT *
			FROM {cls.TABLE}
			WHERE {SupplyItem.COLUMN_SUPPLY_ID} = %s
		"""
		cur.execute(query, (supply_id,))
		return [SupplyItem(**row) for row in cur.fetchall()]
	
	@classmethod
	def get_many_by_product_id(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		limit: int = 50,
		offset: int = 0
	) -> tuple[list[SupplyItem], int]:
		items = cls.select_many(
			cur=cur,
			equals={SupplyItem.COLUMN_PRODUCT_ID: product_id},
			limit=limit,
			offset=offset
		)

		query = f"""
			SELECT COUNT(*) as total
			FROM {cls.TABLE}
			WHERE {SupplyItem.COLUMN_PRODUCT_ID} = %s
		"""
		cur.execute(query, (product_id,))
		return (items, cur.fetchone()['total'],)
	
	@classmethod
	def get_total_price(
		cls,
		cur: psycopg.Cursor,
		supply_id: int
	) -> Decimal:
		query = f"""
			SELECT COALESCE(
				SUM(si.{SupplyItem.COLUMN_PRICE} * si.{SupplyItem.COLUMN_QUANTITY}),
					0
			) AS total
			FROM {SupplyItem.TABLE} si
			WHERE si.{SupplyItem.COLUMN_SUPPLY_ID} = %s
		"""
		cur.execute(query, (supply_id,))
		row = cur.fetchone()
		return Decimal(row["total"])
