import psycopg
from app.types.supply_status import SupplyStatus
from app.repositories.base.base_repository import BaseRepository
from app.models.public.supply_status_history import SupplyStatusHistory
from app.repositories.base.mixins.selectable_mixin import SelectableMixin


class SupplyStatusHistoryRepository(
	BaseRepository,
	SelectableMixin[SupplyStatusHistory]
):
	TABLE = "supply_status_history"
	MODEL = SupplyStatusHistory
	TABLE_COLUMNS = (
		"id",
		"supply_id",
		"status",
		"changed_by",
		"changed_at",
	)

	# warning: get_latest_by_supply_id uses this class var!
	ORDER_BY = (("changed_at", "DESC"), ("id", "DESC",),)

	@classmethod
	def create(
		cls,
		cur: psycopg.Cursor,
		supply_id: int,
		status: SupplyStatus,
		changed_by: int | None
	) -> int:
		return cls.execute_create(
			cur=cur,
			table=cls.TABLE,
			fields={
				"supply_id": supply_id,
				"status": status,
				"changed_by": changed_by
			},
			returning="id"
		)["id"]
	
	@classmethod
	def get_by_id(cls, cur: psycopg.Cursor, supply_status_history_id: int) -> SupplyStatusHistory | None:
		return cls.select(cur=cur, equals={"id": supply_status_history_id})
	
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
			equals={"supply_id": supply_id},
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
			equals={"supply_id": supply_id},
			limit=1,
			offset=0
		)

		return res[0] if res else None
