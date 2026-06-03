import psycopg
from typing import ClassVar
from app.models.public.supply import Supply
from app.types.supply_status import SupplyStatus
from app.types.update_result import UpdateResult
from datetime import date, datetime, time, timedelta
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
	) -> tuple[list[Supply], int]:
		supplies = cls.select_many(
			cur=cur,
			equals={Supply.COLUMN_SUPPLIER_ID: supplier_id},
			limit=limit,
			offset=offset
		)

		query = f"""
			SELECT COUNT(*) as total
			FROM {cls.TABLE}
			WHERE {Supply.COLUMN_SUPPLIER_ID} = %s
		"""
		cur.execute(query, (supplier_id,))
		return (supplies, cur.fetchone()['total'],)
	
	@classmethod
	def get_many_by_warehouse_id(
		cls,
		cur: psycopg.Cursor,
		warehouse_id: int,
		limit: int = 50,
		offset: int = 0
	) -> tuple[list[Supply], int]:
		supplies = cls.select_many(
			cur=cur,
			equals={Supply.COLUMN_WAREHOUSE_ID: warehouse_id},
			limit=limit,
			offset=offset
		)

		query = f"""
			SELECT COUNT(*) as total
			FROM {cls.TABLE}
			WHERE {Supply.COLUMN_WAREHOUSE_ID} = %s
		"""
		cur.execute(query, (warehouse_id,))
		return (supplies, cur.fetchone()['total'],)

	@classmethod
	def search(
		cls,
		cur: psycopg.Cursor,
		status: SupplyStatus | None = None,
		created_from: date | None = None,
		created_to: date | None = None,
		planned_delivery_from: date | None = None,
		planned_delivery_to: date | None = None,
		limit: int = 50,
		offset: int = 0
	) -> tuple[list[Supply], int]:
		limit, offset = Utils.normalize_pagination(limit, offset)
		conditions = []
		params = []
		if status is not None:
			conditions.append(f"{Supply.COLUMN_CURRENT_STATUS} = %s")
			params.append(status)
		if created_from is not None:
			conditions.append(f"{Supply.COLUMN_CREATED_AT} >= %s")
			params.append(datetime.combine(created_from, time.min))
		if created_to is not None:
			conditions.append(f"{Supply.COLUMN_CREATED_AT} < %s")
			params.append(datetime.combine(created_to + timedelta(days=1), time.min))
		if planned_delivery_from is not None:
			conditions.append(f"{Supply.COLUMN_PLANNED_DELIVERY_DATE} >= %s")
			params.append(planned_delivery_from)
		if planned_delivery_to is not None:
			conditions.append(f"{Supply.COLUMN_PLANNED_DELIVERY_DATE} <= %s")
			params.append(planned_delivery_to)
		
		query = Utils.build_select_statement(
			select_fields=cls.TABLE_COLUMNS,
			table=cls.TABLE,
			conditions=tuple(conditions),
			order_by=cls.ORDER_BY,
			many=True
		)

		cur.execute(query, (*params, limit, offset,))
		supplies = [Supply(**row) for row in cur.fetchall()]

		query = f"""
			SELECT COUNT(*) as total
			FROM {cls.TABLE}
			{Utils.build_where(conditions)}
		"""
		cur.execute(query, (*params,))
		return (supplies, cur.fetchone()['total'],)
