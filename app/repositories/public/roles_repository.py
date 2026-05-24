
import psycopg
from app.models.public.role import Role
from app.types.deactivate_result import DeactivateResult
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.selectable_mixin import SelectableMixin
from app.repositories.base.mixins.audit_state_mixin import AuditStateMixin


class RolesRepository(
	BaseRepository,
	AuditStateMixin,
	SelectableMixin[Role]
):
	TABLE = "roles"
	MODEL = Role
	TABLE_COLUMNS = (
		"id",
		"code",
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
		is_system: bool,
		created_by: int | None
	) -> int:
		return cls.execute_create(
			cur=cur,
			table=cls.TABLE,
			fields={
				"code": code,
				"is_system": is_system,
				"created_by": created_by
			},
			returning="id"
		)["id"]
	
	@classmethod
	def deactivate(cls, cur: psycopg.Cursor, role_id: int, deactivated_by: int) -> DeactivateResult:
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
		cur.execute(query, (deactivated_by, role_id,))
		if cur.rowcount != 0:
			return DeactivateResult.SUCCESS
		
		role = cls.get_by_id(cur, role_id)
		if not role:
			return DeactivateResult.FAIL_NOT_FOUND
		
		if role.is_system:
			return DeactivateResult.FAIL_IS_SYSTEM
		return DeactivateResult.SUCCESS
	
	@classmethod
	def restore(cls, cur: psycopg.Cursor, role_id: int) -> bool:
		return cls.clear_state(cur, "deactivated", {"id": role_id})
	
	@classmethod
	def get_by_id(cls, cur: psycopg.Cursor, role_id: int) -> Role | None:
		return cls.select(cur=cur, equals={"id": role_id})
	
	@classmethod
	def get_by_code(cls, cur: psycopg.Cursor, code: str) -> Role | None:
		return cls.select(cur=cur, equals={"code": code})
	
	@classmethod
	def search(
		cls,
		cur: psycopg.Cursor,
		search: str | None = None,
		exclude_deactivated: bool = True,
		limit: int = 50,
		offset: int = 0
	) -> list[Role]:
		return cls.select_many(
			cur=cur,
			is_null=("deactivated_at",) if exclude_deactivated else None,
			ilike=(("code",), f"%{search}%",) if search else None,
			limit=limit,
			offset=offset
		)