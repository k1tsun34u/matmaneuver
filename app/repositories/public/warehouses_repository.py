
import psycopg
from app.types.update_result import UpdateResult
from app.models.public.warehouse import Warehouse
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.updatable_mixin import UpdatableMixin
from app.repositories.base.mixins.selectable_mixin import SelectableMixin
from app.repositories.base.mixins.audit_state_mixin import AuditStateMixin


class WarehousesRepository(
	BaseRepository,
	AuditStateMixin,
	UpdatableMixin,
	SelectableMixin[Warehouse]
):
	TABLE = "warehouses"
	MODEL = Warehouse
	TABLE_COLUMNS = (
		Warehouse.COLUMN_ID,
		Warehouse.COLUMN_ADDRESS,
		Warehouse.COLUMN_DESCRIPTION,
		Warehouse.COLUMN_DELETED_BY,
		Warehouse.COLUMN_DELETED_AT,
		Warehouse.COLUMN_CREATED_BY,
		Warehouse.COLUMN_CREATED_AT,
	)

	ORDER_BY = ((Warehouse.COLUMN_CREATED_AT, "DESC"),)

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
				Warehouse.COLUMN_ADDRESS: address,
				Warehouse.COLUMN_DESCRIPTION: description,
				Warehouse.COLUMN_CREATED_BY: created_by
			},
			returning=Warehouse.COLUMN_ID
		)[Warehouse.COLUMN_ID]
	
	@classmethod
	def set_description(
		cls,
		cur: psycopg.Cursor,
		warehouse_id: int,
		description: str | None
	) -> UpdateResult:
		return cls.update_by_conditions(
			cur=cur,
			identity_where={Warehouse.COLUMN_ID: warehouse_id},
			condition_where={},
			fields={Warehouse.COLUMN_DESCRIPTION: description}
		)
	
	@classmethod
	def soft_delete(cls, cur: psycopg.Cursor, warehouse_id: int, deleted_by: int | None) -> UpdateResult:
		return cls.set_state(cur, "deleted", {Warehouse.COLUMN_ID: warehouse_id}, deleted_by)
	
	@classmethod
	def restore(cls, cur: psycopg.Cursor, warehouse_id: int) -> UpdateResult:
		return cls.clear_state(cur, "deleted", {Warehouse.COLUMN_ID: warehouse_id})
	
	@classmethod
	def get_by_id(cls, cur: psycopg.Cursor, warehouse_id: int) -> Warehouse | None:
		return cls.select(cur=cur, equals={Warehouse.COLUMN_ID: warehouse_id})
	
	@classmethod
	def get_by_address(cls, cur: psycopg.Cursor, address: str) -> Warehouse | None:
		return cls.select(cur=cur, equals={Warehouse.COLUMN_ADDRESS: address})
	
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
			is_null=(Warehouse.COLUMN_DELETED_AT,) if exclude_deleted else None,
			ilike=((Warehouse.COLUMN_ADDRESS, Warehouse.COLUMN_DESCRIPTION,), f"%{search}%",) if search else None,
			limit=limit,
			offset=offset
		)
