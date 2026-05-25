import psycopg
from typing import ClassVar
from app.types.supply_status import SupplyStatus
from app.repositories.base.base_repository import BaseRepository
from app.models.public.supply_status_history import SupplyStatusHistory
from app.repositories.base.mixins.selectable_mixin import SelectableMixin


class SupplyStatusHistoryRepository(
	BaseRepository,
	SelectableMixin[SupplyStatusHistory]
):
	TABLE: ClassVar[str] = SupplyStatusHistory.TABLE
	MODEL = SupplyStatusHistory
	TABLE_COLUMNS = (
		SupplyStatusHistory.COLUMN_ID,
		SupplyStatusHistory.COLUMN_SUPPLY_ID,
		SupplyStatusHistory.COLUMN_STATUS,
		SupplyStatusHistory.COLUMN_CHANGED_BY,
		SupplyStatusHistory.COLUMN_CHANGED_AT,
	)

	# warning: get_latest_by_supply_id uses this class var!
	ORDER_BY = (
		(SupplyStatusHistory.COLUMN_CHANGED_AT, "DESC",),
		(SupplyStatusHistory.COLUMN_ID, "DESC",),
	)

	@classmethod
	def create(
		cls,
		cur: psycopg.Cursor,
		supply_id: int,
		status: SupplyStatus,
		set_by: int | None
	) -> int:
		return cls.execute_create(
			cur=cur,
			table=cls.TABLE,
			fields={
				SupplyStatusHistory.COLUMN_SUPPLY_ID: supply_id,
				SupplyStatusHistory.COLUMN_STATUS: status,
				SupplyStatusHistory.COLUMN_CHANGED_BY: set_by
			},
			returning=SupplyStatusHistory.COLUMN_ID
		)[SupplyStatusHistory.COLUMN_ID]
	
	@classmethod
	def get_by_id(cls, cur: psycopg.Cursor, supply_status_history_id: int) -> SupplyStatusHistory | None:
		return cls.select(cur=cur, equals={SupplyStatusHistory.COLUMN_ID: supply_status_history_id})
	
	@classmethod
	def get_many_by_supply_id(
		cls,
		cur: psycopg.Cursor,
		supply_id: int,
		limit: int = 50,
		offset: int = 0,
	) -> list[SupplyStatusHistory]:
		return cls.select_many(
			cur=cur,
			equals={SupplyStatusHistory.COLUMN_SUPPLY_ID: supply_id},
			limit=limit,
			offset=offset
		)
	
	@classmethod
	def get_latest_by_supply_id(
		cls,
		cur: psycopg.Cursor,
		supply_id: int
	) -> SupplyStatusHistory | None:
		res = cls.select_many(
			cur=cur,
			equals={SupplyStatusHistory.COLUMN_SUPPLY_ID: supply_id},
			limit=1,
			offset=0
		)

		return res[0] if res else None
