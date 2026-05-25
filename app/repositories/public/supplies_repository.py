import psycopg
from datetime import date
from typing import ClassVar
from app.models.public.supply import Supply
from app.types.supply_status import SupplyStatus
from app.types.update_result import UpdateResult
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.updatable_mixin import UpdatableMixin
from app.repositories.base.mixins.selectable_mixin import SelectableMixin
from app.utils import Utils


class SuppliesRepository(
	BaseRepository,
	UpdatableMixin,
	SelectableMixin[Supply]
):
	TABLE: ClassVar[str] = Supply.TABLE
	MODEL = Supply
	TABLE_COLUMNS = (
		Supply.COLUMN_ID,
		Supply.COLUMN_SUPPLIER_ID,
		Supply.COLUMN_WAREHOUSE_ID,
		Supply.COLUMN_CURRENT_STATUS,
		Supply.COLUMN_PLANNED_DELIVERY_DATE,
		Supply.COLUMN_CREATED_BY,
		Supply.COLUMN_CREATED_AT,
	)

	ORDER_BY = ((Supply.COLUMN_CREATED_AT, "DESC",),)

	@classmethod
	def create(
		cls,
		cur: psycopg.Cursor,
		supplier_id: int,
		warehouse_id: int,
		planned_delivery_date: date,
		created_by: int | None
	) -> int:
		return cls.execute_create(
			cur=cur,
			table=cls.TABLE,
			fields={
				Supply.COLUMN_SUPPLIER_ID: supplier_id,
				Supply.COLUMN_WAREHOUSE_ID: warehouse_id,
				Supply.COLUMN_CURRENT_STATUS: SupplyStatus.CREATED,
				Supply.COLUMN_PLANNED_DELIVERY_DATE: planned_delivery_date,
				Supply.COLUMN_CREATED_BY: created_by
			},
			returning=Supply.COLUMN_ID
		)[Supply.COLUMN_ID]
	
	@classmethod
	def set_status(
		cls,
		cur: psycopg.Cursor,
		supply_id: int,
		status: SupplyStatus
	) -> UpdateResult:
		return cls.update_by_conditions(
			cur=cur,
			identity_where={Supply.COLUMN_ID: supply_id},
			condition_where={},
			fields={Supply.COLUMN_CURRENT_STATUS: status}
		)
	
	@classmethod
	def get_by_id(
		cls,
		cur: psycopg.Cursor,
		supply_id: int
	) -> Supply | None:
		return cls.select(cur, {Supply.COLUMN_ID: supply_id})
	
	@classmethod
	def get_by_id_for_update(
		cls,
		cur: psycopg.Cursor,
		supply_id: int
	) -> Supply | None:
		query = f"""
			SELECT {", ".join(cls.TABLE_COLUMNS)}
			FROM {cls.TABLE}
			WHERE {Supply.COLUMN_ID} = %s
			FOR UPDATE
			LIMIT 1
		"""
		cur.execute(query, (supply_id,))
		row = cur.fetchone()
		return Supply(**row) if row else None
	
	@classmethod
	def get_many_by_supplier_id(
		cls,
		cur: psycopg.Cursor,
		supplier_id: int,
		limit: int = 50,
		offset: int = 0
	) -> list[Supply]:
		return cls.select_many(
			cur=cur,
			equals={Supply.COLUMN_SUPPLIER_ID: supplier_id},
			limit=limit,
			offset=offset
		)
	
	@classmethod
	def get_many_by_warehouse_id(
		cls,
		cur: psycopg.Cursor,
		warehouse_id: int,
		limit: int = 50,
		offset: int = 0
	) -> list[Supply]:
		return cls.select_many(
			cur=cur,
			equals={Supply.COLUMN_WAREHOUSE_ID: warehouse_id},
			limit=limit,
			offset=offset
		)
