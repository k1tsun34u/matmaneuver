import psycopg
from datetime import date
from app.models.public.write_off import WriteOff
from app.types.write_off_reason import WriteOffReason
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.selectable_mixin import SelectableMixin
from app.utils import Utils


class WriteOffsRepository(
	BaseRepository,
	SelectableMixin[WriteOff]
):
	TABLE = "write_offs"
	MODEL = WriteOff
	TABLE_COLUMNS = (
		"id",
		"warehouse_id",
		"reason",
		"comment",
		"created_by",
		"created_at",
	)

	ORDER_BY = (("created_at", "DESC"), ("id", "DESC"),)

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
				"warehouse_id": warehouse_id,
				"reason": reason,
				"comment": comment,
				"created_by": created_by
			},
			returning="id"
		)["id"]
	
	@classmethod
	def get_by_id(cls, cur: psycopg.Cursor, write_off_id: int) -> WriteOff | None:
		return cls.select(cur, {"id": write_off_id})
	
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
			conditions.append("comment ILIKE %s")
			params.append(f"%{search}%")
		if warehouse_id is not None:
			conditions.append("warehouse_id = %s")
			params.append(warehouse_id)
		if reason is not None:
			conditions.append("reason = %s")
			params.append(reason)
		if created_from is not None:
			conditions.append("created_at::date >= %s")
			params.append(created_from)
		if created_to is not None:
			conditions.append("created_at::date <= %s")
			params.append(created_to)
		
		query = Utils.build_select_statement(
			select_fields=cls.TABLE_COLUMNS,
			table=cls.TABLE,
			conditions=tuple(conditions),
			order_by=cls.ORDER_BY,
			many=True
		)

		cur.execute(query, (*params, limit, offset,))
		return [WriteOff(**row) for row in cur.fetchall()]
