import psycopg
from typing import ClassVar
from app.models.public.warehouse import Warehouse
from app.models.public.write_off_warehouse import WriteOffWarehouse
from app.utils import Utils
from app.models.public.write_off import WriteOff
from datetime import date, datetime, time, timedelta
from app.types.write_off_reason import WriteOffReason
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.selectable_mixin import SelectableMixin


class WriteOffsRepository(
	BaseRepository,
	SelectableMixin[WriteOff]
):
	TABLE: ClassVar[str] = WriteOff.TABLE
	MODEL = WriteOff
	TABLE_COLUMNS = (
		WriteOff.COLUMN_ID,
		WriteOff.COLUMN_WAREHOUSE_ID,
		WriteOff.COLUMN_REASON,
		WriteOff.COLUMN_COMMENT,
		WriteOff.COLUMN_CREATED_BY,
		WriteOff.COLUMN_CREATED_AT,
	)

	ORDER_BY = (
		(WriteOff.COLUMN_CREATED_AT, "DESC",),
		(WriteOff.COLUMN_ID, "DESC",),
	)

	@classmethod
	def create(
		cls,
		cur: psycopg.Cursor,
		warehouse_id: int,
		reason: WriteOffReason,
		comment: str | None,
		created_by: int | None
	) -> int:
		return cls.execute_create(
			cur=cur,
			table=cls.TABLE,
			fields={
				WriteOff.COLUMN_WAREHOUSE_ID: warehouse_id,
				WriteOff.COLUMN_REASON: reason.value,
				WriteOff.COLUMN_COMMENT: comment,
				WriteOff.COLUMN_CREATED_BY: created_by
			},
			returning=WriteOff.COLUMN_ID
		)[WriteOff.COLUMN_ID]
	
	@classmethod
	def get_by_id(cls, cur: psycopg.Cursor, write_off_id: int) -> WriteOffWarehouse | None:
		query = f"""
			SELECT
				wo.*,
				wh.{Warehouse.COLUMN_ADDRESS} as warehouse_address
			FROM {cls.TABLE} AS wo
			JOIN {Warehouse.TABLE} wh ON wh.{Warehouse.COLUMN_ID} = wo.{WriteOff.COLUMN_WAREHOUSE_ID}
			WHERE wo.{WriteOff.COLUMN_ID} = %s
		"""
		cur.execute(query, (write_off_id,))
		row = cur.fetchone()
		return WriteOffWarehouse(**row) if row else None
	
	@classmethod
	def get_many_by_warehouse_id(
		cls,
		cur: psycopg.Cursor,
		warehouse_id: int,
		limit: int = 50,
		offset: int = 0
	) -> tuple[list[WriteOff], int]:
		write_offs = cls.select_many(
			cur=cur,
			equals={WriteOff.COLUMN_WAREHOUSE_ID: warehouse_id},
			limit=limit,
			offset=offset
		)
		
		query = f"""
			SELECT COUNT(*) as total
			FROM {cls.TABLE}
			WHERE {WriteOff.COLUMN_WAREHOUSE_ID} = %s
		"""
		cur.execute(query, (warehouse_id,))
		return (write_offs, cur.fetchone()['total'],)
	
	@classmethod
	def search(
		cls,
		cur: psycopg.Cursor,
		search: str | None = None,
		warehouse_id: int | None = None,
		reason: WriteOffReason | None = None,
		created_from: date | None = None,
		created_to: date | None = None,
		limit: int = 50,
		offset: int = 0
	) -> list[WriteOff]:
		limit, offset = Utils.normalize_pagination(limit, offset)
		conditions = []
		params = []
		if search:
			conditions.append(f"{WriteOff.COLUMN_COMMENT} ILIKE %s")
			params.append(f"%{search}%")
		if warehouse_id is not None:
			conditions.append(f"{WriteOff.COLUMN_WAREHOUSE_ID} = %s")
			params.append(warehouse_id)
		if reason is not None:
			conditions.append(f"{WriteOff.COLUMN_REASON} = %s")
			params.append(reason.value)
		if created_from is not None:
			conditions.append(f"{WriteOff.COLUMN_CREATED_AT} >= %s")
			params.append(datetime.combine(created_from, time.min))
		if created_to is not None:
			conditions.append(f"{WriteOff.COLUMN_CREATED_AT} < %s")
			params.append(datetime.combine(created_to + timedelta(days=1), time.min))
		
		query = Utils.build_select_statement(
			select_fields=cls.TABLE_COLUMNS,
			table=cls.TABLE,
			conditions=tuple(conditions),
			order_by=cls.ORDER_BY,
			many=True
		)

		cur.execute(query, (*params, limit, offset,))
		write_offs = [WriteOff(**row) for row in cur.fetchall()]
		
		query = f"""
			SELECT COUNT(*) as total
			FROM {cls.TABLE}
			{Utils.build_where(conditions)}
		"""
		cur.execute(query, (*params,))
		return (write_offs, cur.fetchone()['total'],)
