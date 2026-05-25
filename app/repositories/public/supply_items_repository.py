import psycopg
from decimal import Decimal
from app.models.public.supply_item import SupplyItem
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.selectable_mixin import SelectableMixin


class SupplyItemsRepository(
	BaseRepository,
	SelectableMixin[SupplyItem]
):
	TABLE = "supply_items"
	MODEL = SupplyItem
	TABLE_COLUMNS = (
		"id",
		"supply_id",
		"product_id",
		"quantity",
		"price",
	)

	ORDER_BY = (("id", "ASC",),)

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
				"supply_id": supply_id,
				"product_id": product_id,
				"quantity": quantity,
				"price": price
			},
			returning="id"
		)["id"]
	
	@classmethod
	def get_by_id(cls, cur: psycopg.Cursor, supply_item_id: int) -> SupplyItem | None:
		return cls.select(cur, {"id": supply_item_id})
	
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
			equals={"supply_id": supply_id},
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
			equals={"product_id": product_id},
			limit=limit,
			offset=offset
		)
