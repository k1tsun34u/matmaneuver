
import psycopg
from app.models.public.warehouse import Warehouse
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.selectable_mixin import SelectableMixin
from app.repositories.base.mixins.audit_state_mixin import AuditStateMixin


class WarehousesRepository(
	BaseRepository,
	AuditStateMixin,
	SelectableMixin[Warehouse]
):
	TABLE = "warehouses"
	MODEL = Warehouse
	SELECT_FIELDS = (
		"id",
		"address",
		"description",
		"deleted_by",
		"deleted_at",
		"created_by",
		"created_at",
	)

	ORDER_BY = (("created_at", "DESC"),)

	@classmethod
	def create(
		cls,
		cur: psycopg.Cursor,
		address: str,
		description: str | None,
		created_by: int | None
	) -> int:
		return cls.execute_create(
			cur=cur,
			table=cls.TABLE,
			fields={
				"address": address,
				"description": description,
				"created_by": created_by
			},
			returning="id"
		)["id"]
	
	@classmethod
	def soft_delete(cls, cur: psycopg.Cursor, warehouse_id: int, deleted_by: int) -> int:
		return cls.set_state(cur, "deleted", {"id": warehouse_id}, deleted_by)
	
	@classmethod
	def restore(cls, cur: psycopg.Cursor, warehouse_id: int) -> int:
		return cls.clear_state(cur, "deleted", {"id": warehouse_id})
	
	@classmethod
	def get_by_id(cls, cur: psycopg.Cursor, warehouse_id: int) -> Warehouse | None:
		return cls.select(cur, {"id": warehouse_id})
	
	@classmethod
	def get_by_address(cls, cur: psycopg.Cursor, address: str) -> Warehouse | None:
		return cls.select(cur, {"address": address})
	
	@classmethod
	def search(
		cls,
		cur: psycopg.Cursor,
		search: str | None = None,
		exclude_deleted: bool = True,
		limit: int = 50,
		offset: int = 0
	) -> list[Warehouse]:
		return cls.select_many(
			cur=cur,
			is_null=("deleted_at",) if exclude_deleted else None,
			ilike=(("address", "description",), f"%{search}%",) if search else None,
			limit=limit,
			offset=offset
		)