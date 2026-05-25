import psycopg
from typing import ClassVar
from app.types.update_result import UpdateResult
from app.models.public.permission import Permission
from app.types.deactivate_result import DeactivateResult
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.updatable_mixin import UpdatableMixin
from app.repositories.base.mixins.selectable_mixin import SelectableMixin
from app.repositories.base.mixins.audit_state_mixin import AuditStateMixin


class PermissionsRepository(
	BaseRepository,
	AuditStateMixin,
	UpdatableMixin,
	SelectableMixin[Permission]
):
	TABLE: ClassVar[str] = Permission.TABLE
	MODEL = Permission
	TABLE_COLUMNS = (
		Permission.COLUMN_ID,
		Permission.COLUMN_CODE,
		Permission.COLUMN_DESCRIPTION,
		Permission.COLUMN_IS_SYSTEM,
		Permission.COLUMN_DEACTIVATED_BY,
		Permission.COLUMN_DEACTIVATED_AT,
		Permission.COLUMN_CREATED_BY,
		Permission.COLUMN_CREATED_AT,
	)

	ORDER_BY = ((Permission.COLUMN_CREATED_AT, "DESC",),)

	@classmethod
	def create(
		cls,
		cur: psycopg.Cursor,
		code: str,
		description: str | None,
		is_system: bool,
		created_by: int | None
	) -> int:
		return cls.execute_create(
			cur=cur,
			table=Permission.TABLE,
			fields={
				Permission.COLUMN_CODE: code,
				Permission.COLUMN_DESCRIPTION: description,
				Permission.COLUMN_IS_SYSTEM: is_system,
				Permission.COLUMN_CREATED_BY: created_by
			},
			returning=Permission.COLUMN_ID
		)[Permission.COLUMN_ID]
	
	@classmethod
	def set_description(
		cls,
		cur: psycopg.Cursor,
		permission_id: int,
		description: str | None
	) -> UpdateResult:
		return cls.update_by_conditions(
			cur=cur,
			identity_where={Permission.COLUMN_ID: permission_id},
			condition_where={},
			fields={Permission.COLUMN_DESCRIPTION: description}
		)
	
	@classmethod
	def deactivate(cls, cur: psycopg.Cursor, permission_id: int, deactivated_by: int) -> DeactivateResult:
		query = f"""
			UPDATE {Permission.TABLE}
			SET
				{Permission.COLUMN_DEACTIVATED_BY} = %s,
				{Permission.COLUMN_DEACTIVATED_AT} = NOW()
			WHERE
				{Permission.COLUMN_ID} = %s
				AND {Permission.COLUMN_IS_SYSTEM} = FALSE
				AND {Permission.COLUMN_DEACTIVATED_AT} IS NULL
		"""
		cur.execute(query, (deactivated_by, permission_id,))
		if cur.rowcount != 0:
			return DeactivateResult.SUCCESS
		
		permission = cls.get_by_id(cur, permission_id)
		if not permission:
			return DeactivateResult.FAIL_NOT_FOUND
		
		if permission.is_system:
			return DeactivateResult.FAIL_IS_SYSTEM
		return DeactivateResult.SUCCESS
	
	@classmethod
	def restore(cls, cur: psycopg.Cursor, permission_id: int) -> UpdateResult:
		return cls.clear_state(cur, "deactivated", {Permission.COLUMN_ID: permission_id})
	
	@classmethod
	def get_by_id(cls, cur: psycopg.Cursor, permission_id: int) -> Permission | None:
		return cls.select(cur=cur, equals={Permission.COLUMN_ID: permission_id})
	
	@classmethod
	def get_by_code(cls, cur: psycopg.Cursor, code: str) -> Permission | None:
		return cls.select(cur=cur, equals={Permission.COLUMN_CODE: code})
	
	@classmethod
	def search(
		cls,
		cur: psycopg.Cursor,
		search: str | None = None,
		exclude_deactivated: bool = True,
		limit: int = 50,
		offset: int = 0
	) -> list[Permission]:
		return cls.select_many(
			cur=cur,
			is_null=(Permission.COLUMN_DEACTIVATED_AT,) if exclude_deactivated else None,
			ilike=((Permission.COLUMN_CODE, Permission.COLUMN_DESCRIPTION,), f"%{search}%",) if search else None,
			limit=limit,
			offset=offset
		)
