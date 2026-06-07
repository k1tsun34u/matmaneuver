
import psycopg
from app.models.public.employee import Employee
from app.models.public.employee_role import EmployeeRole
from app.utils import Utils
from typing import ClassVar
from app.models.public.role import Role
from app.types.update_result import UpdateResult
from app.types.deactivate_result import DeactivateResult
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.selectable_mixin import SelectableMixin
from app.repositories.base.mixins.audit_state_mixin import AuditStateMixin


class RolesRepository(
	BaseRepository,
	AuditStateMixin,
	SelectableMixin[Role]
):
	TABLE: ClassVar[str] = Role.TABLE
	MODEL = Role
	TABLE_COLUMNS = (
		Role.COLUMN_ID,
		Role.COLUMN_CODE,
		Role.COLUMN_IS_SYSTEM,
		Role.COLUMN_DEACTIVATED_BY,
		Role.COLUMN_DEACTIVATED_AT,
		Role.COLUMN_CREATED_BY,
		Role.COLUMN_CREATED_AT,
	)

	ORDER_BY = ((Role.COLUMN_CREATED_AT, "DESC",),)

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
			table=Role.TABLE,
			fields={
				Role.COLUMN_CODE: code,
				Role.COLUMN_IS_SYSTEM: is_system,
				Role.COLUMN_CREATED_BY: created_by
			},
			returning=Role.COLUMN_ID
		)[Role.COLUMN_ID]
	
	@classmethod
	def deactivate(cls, cur: psycopg.Cursor, role_id: int, deactivated_by: int) -> DeactivateResult:
		query = f"""
			UPDATE {Role.TABLE}
			SET
				{Role.COLUMN_DEACTIVATED_BY} = %s,
				{Role.COLUMN_DEACTIVATED_AT} = NOW()
			WHERE
				{Role.COLUMN_ID} = %s
				AND {Role.COLUMN_IS_SYSTEM} = FALSE
				AND {Role.COLUMN_DEACTIVATED_AT} IS NULL
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
	def restore(cls, cur: psycopg.Cursor, role_id: int) -> UpdateResult:
		return cls.clear_state(cur, "deactivated", {Role.COLUMN_ID: role_id})
	
	@classmethod
	def get_by_id(cls, cur: psycopg.Cursor, role_id: int) -> Role | None:
		return cls.select(cur=cur, equals={Role.COLUMN_ID: role_id})
	
	@classmethod
	def get_by_code(cls, cur: psycopg.Cursor, code: str) -> Role | None:
		return cls.select(cur=cur, equals={Role.COLUMN_CODE: code})
	
	@classmethod
	def get_all_by_employee_id(cls, cur: psycopg.Cursor, employee_id: int) -> list[Role]:
		equals = {f'er.{EmployeeRole.COLUMN_EMPLOYEE_ID}': employee_id}
		is_null = (f'r.{Role.COLUMN_DEACTIVATED_AT}',)

		conditions, params = Utils.build_conditions_params(
			equals=equals,
			is_null=is_null
		)

		query = f"""
			SELECT r.*
			FROM {cls.TABLE} r
			JOIN {EmployeeRole.TABLE} er ON er.{EmployeeRole.COLUMN_ROLE_ID} = r.{Role.COLUMN_ID}
			{Utils.build_where(conditions)}
			{Utils.build_order_by(cls.ORDER_BY)}
		"""
		cur.execute(query, params)
		return [Role(**row) for row in cur.fetchall()]
	
	@classmethod
	def search(
		cls,
		cur: psycopg.Cursor,
		search: str | None = None,
		exclude_deactivated: bool = True,
		limit: int = 50,
		offset: int = 0
	) -> tuple[list[Role], int]:
		norm_search = Utils.normalize_code(search) if search else None
		is_null = (Role.COLUMN_DEACTIVATED_AT,) if exclude_deactivated else None
		ilike = ((Role.COLUMN_CODE,), f"%{norm_search}%",) if norm_search else None
		roles =  cls.select_many(
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
		return (roles, cur.fetchone()['total'],)
