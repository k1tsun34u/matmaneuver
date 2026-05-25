import psycopg
from typing import ClassVar
from decimal import Decimal
from app.models.public.product import Product
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
	) -> list[SupplyItem]:
		return cls.select_many(
			cur=cur,
			equals={SupplyItem.COLUMN_SUPPLY_ID: supply_id},
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
	) -> list[SupplyItem]:
		return cls.select_many(
			cur=cur,
			equals={SupplyItem.COLUMN_PRODUCT_ID: product_id},
			limit=limit,
			offset=offset
		)
	
	@classmethod
	def get_products_by_supply_id(
		cls,
		cur: psycopg.Cursor,
		supply_id: int
	) -> list[Product]:
		query = f"""
			SELECT p.*
			FROM {Product.TABLE} p
			JOIN {SupplyItem.TABLE} si ON si.{SupplyItem.COLUMN_PRODUCT_ID} = p.{Product.COLUMN_ID}
			WHERE si.{SupplyItem.COLUMN_SUPPLY_ID} = %s
		"""
		cur.execute(query, (supply_id,))
		return [Product(**row) for row in cur.fetchall()]
