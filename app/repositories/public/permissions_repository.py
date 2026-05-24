import psycopg
from app.models.public.permission import Permission
from app.types.deactivate_result import DeactivateResult
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.selectable_mixin import SelectableMixin
from app.repositories.base.mixins.audit_state_mixin import AuditStateMixin


class PermissionsRepository(
	BaseRepository,
	AuditStateMixin,
	SelectableMixin[Permission]
):
	TABLE = "permissions"
	MODEL = Permission
	TABLE_COLUMNS = (
		"id",
		"code",
		"description",
		"is_system",
		"deactivated_by",
		"deactivated_at",
		"created_by",
		"created_at",
	)

	ORDER_BY = (("created_at", "DESC"),)

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
			table=cls.TABLE,
			fields={
				"code": code,
				"description": description,
				"is_system": is_system,
				"created_by": created_by
			},
			returning="id"
		)["id"]
	
	@classmethod
	def set_description(
		cls,
		cur: psycopg.Cursor,
		permission_id: int,
		description: str
	) -> bool:
		cls.execute_update(
			cur=cur,
			table=cls.TABLE,
			where={"id": permission_id},
			fields={"description": description}
		)

		cur.execute(f"SELECT 1 FROM {cls.TABLE} WHERE id = %s", (permission_id,))
		return bool(cur.fetchone())
	
	@classmethod
	def deactivate(cls, cur: psycopg.Cursor, permission_id: int, deactivated_by: int) -> DeactivateResult:
		query = f"""
			UPDATE {cls.TABLE}
			SET
				deactivated_by = %s,
				deactivated_at = NOW()
			WHERE
				id = %s
				AND is_system = FALSE
				AND deactivated_at IS NULL
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
	def restore(cls, cur: psycopg.Cursor, permission_id: int) -> int:
		return cls.clear_state(cur, "deactivated", {"id": permission_id})
	
	@classmethod
	def get_by_id(cls, cur: psycopg.Cursor, permission_id: int) -> Permission | None:
		return cls.select(cur=cur, equals={"id": permission_id})
	
	@classmethod
	def get_by_code(cls, cur: psycopg.Cursor, code: str) -> Permission | None:
		return cls.select(cur=cur, equals={"code": code})
	
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
			is_null=("deactivated_at",) if exclude_deactivated else None,
			ilike=(("code", "description",), f"%{search}%",) if search else None,
			limit=limit,
			offset=offset
		)