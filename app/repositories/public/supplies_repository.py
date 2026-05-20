import psycopg
from datetime import date
from app.models.public.supply import Supply
from app.types.supply_status import SupplyStatus
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.selectable_mixin import SelectableMixin


class SuppliesRepository(
	BaseRepository,
	SelectableMixin[Supply]
):
	TABLE = "supplies"
	MODEL = Supply
	SELECT_FIELDS = (
		"id",
		"supplier_id",
		"warehouse_id",
		"current_status",
		"planned_delivery_date",
		"created_by",
		"created_at",
	)

	ORDER_BY = (("created_at", "DESC"),)

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
				"supplier_id": supplier_id,
				"warehouse_id": warehouse_id,
				"current_status": SupplyStatus.CREATED,
				"planned_delivery_date": planned_delivery_date,
				"created_by": created_by
			},
			returning="id"
		)["id"]
	
	@classmethod
	def change_status(
		cls,
		cur: psycopg.Cursor,
		supply_id: int,
		status: SupplyStatus
	) -> int:
		return cls.execute_update(
			cur=cur,
			table=cls.TABLE,
			where={"id": supply_id},
			fields={"current_status": status}
		)
	
	@classmethod
	def get_by_id(
		cls,
		cur: psycopg.Cursor,
		supply_id: int
	) -> Supply | None:
		return cls.select(cur, {"id": supply_id})
