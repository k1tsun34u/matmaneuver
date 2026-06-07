import psycopg
from typing import ClassVar
from app.models.public.role import Role
from app.models.public.role_permission import RolePermission
from app.types.update_result import UpdateResult
from app.models.public.permission import Permission
from app.types.deactivate_result import DeactivateResult
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.updatable_mixin import UpdatableMixin
from app.repositories.base.mixins.selectable_mixin import SelectableMixin
from app.repositories.base.mixins.audit_state_mixin import AuditStateMixin
from app.utils import Utils


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
	def get_all_by_role_id(
		cls,
		cur: psycopg.Cursor,
		role_id: int
	) -> list[Permission]:
		equals = {f'rp.{RolePermission.COLUMN_ROLE_ID}': role_id}
		is_null=(f'p.{Permission.COLUMN_DEACTIVATED_AT}',)

		conditions, params = Utils.build_conditions_params(
			equals=equals,
			is_null=is_null
		)

		query = f"""
			SELECT p.*
			FROM {cls.TABLE} p
			JOIN {RolePermission.TABLE} rp ON rp.{RolePermission.COLUMN_PERMISSION_ID} = p.{Permission.COLUMN_ID}
			JOIN {Role.TABLE} r ON r.{Role.COLUMN_ID} = rp.{RolePermission.COLUMN_ROLE_ID}
			{Utils.build_where(conditions)}
			{Utils.build_order_by(cls.ORDER_BY)}
		"""
		cur.execute(query, params)
		return [Permission(**row) for row in cur.fetchall()]
	
	@classmethod
	def search(
		cls,
		cur: psycopg.Cursor,
		search: str | None = None,
		exclude_deactivated: bool = True,
		limit: int = 50,
		offset: int = 0
	) -> tuple[list[Permission], int]:
		is_null=(Permission.COLUMN_DEACTIVATED_AT,) if exclude_deactivated else None
		ilike=((Permission.COLUMN_CODE, Permission.COLUMN_DESCRIPTION,), f"%{search}%",) if search else None
		permissions = cls.select_many(
			cur=cur,
			is_null=is_null,
			ilike=ilike,
			limit=limit,
			offset=offset
		)

		conditions, params = Utils.build_conditions_params(
			is_null=is_null,
			ilike=ilike
		)

		query = f"""
			SELECT COUNT(*) AS total
			FROM {cls.TABLE}
			{Utils.build_where(conditions)}
		"""
		cur.execute(query, params)
		return (permissions, cur.fetchone()['total'],)
