import psycopg
from typing import ClassVar
from collections.abc import Sequence
from app.models.public.role import Role
from app.models.public.employee import Employee
from app.models.public.employee_role import EmployeeRole
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.relation_mixin import RelationMixin
from app.repositories.base.mixins.selectable_mixin import SelectableMixin


class EmployeeRolesRepository(
	BaseRepository,
	RelationMixin,
	SelectableMixin[EmployeeRole]
):
	TABLE: ClassVar[str] = EmployeeRole.TABLE
	MODEL = EmployeeRole
	TABLE_COLUMNS = (
		EmployeeRole.COLUMN_EMPLOYEE_ID,
		EmployeeRole.COLUMN_ROLE_ID,
		EmployeeRole.COLUMN_ASSIGNED_BY,
		EmployeeRole.COLUMN_ASSIGNED_AT,
	)

	ORDER_BY = ((EmployeeRole.COLUMN_ASSIGNED_AT, "DESC",),)

	@classmethod
	def assign(
		cls,
		cur: psycopg.Cursor,
		employee_id: int,
		role_id: int,
		assigned_by: int | None
	) -> None:
		cls.create_relation(
			cur=cur,
			fixed_field=EmployeeRole.COLUMN_EMPLOYEE_ID,
			fixed_value=employee_id,
			varying_field=EmployeeRole.COLUMN_ROLE_ID,
			varying_value=role_id,
			actor_id=assigned_by
		)
	
	@classmethod
	def unassign(
		cls,
		cur: psycopg.Cursor,
		employee_id: int,
		role_id: int
	) -> None:
		cls.delete_relation(
			cur=cur,
			fixed_field=EmployeeRole.COLUMN_EMPLOYEE_ID,
			fixed_value=employee_id,
			varying_field=EmployeeRole.COLUMN_ROLE_ID,
			varying_value=role_id
		)
	
	@classmethod
	def assign_many(
		cls,
		cur: psycopg.Cursor,
		employee_id: int,
		role_ids: Sequence[int],
		assigned_by: int | None
	) -> None:
		cls.create_relations(
			cur=cur,
			fixed_field=EmployeeRole.COLUMN_EMPLOYEE_ID,
			fixed_value=employee_id,
			varying_field=EmployeeRole.COLUMN_ROLE_ID,
			varying_values=role_ids,
			actor_id=assigned_by
		)
	
	@classmethod
	def unassign_many(
		cls,
		cur: psycopg.Cursor,
		employee_id: int,
		role_ids: Sequence[int]
	) -> None:
		cls.delete_relations(
			cur=cur,
			fixed_field=EmployeeRole.COLUMN_EMPLOYEE_ID,
			fixed_value=employee_id,
			varying_field=EmployeeRole.COLUMN_ROLE_ID,
			varying_values=role_ids
		)
	
	@classmethod
	def get_by_employee_id_role_id(
		cls,
		cur: psycopg.Cursor,
		employee_id: int,
		role_id: int
	) -> EmployeeRole | None:
		return cls.select(cur, {EmployeeRole.COLUMN_EMPLOYEE_ID: employee_id, EmployeeRole.COLUMN_ROLE_ID: role_id})
	
	@classmethod
	def get_many_by_employee_id(cls, cur: psycopg.Cursor, employee_id: int) -> list[EmployeeRole]:
		return cls.select_many(cur, {EmployeeRole.COLUMN_EMPLOYEE_ID: employee_id})
	
	@classmethod
	def get_many_by_role_id(cls, cur: psycopg.Cursor, role_id: int) -> list[EmployeeRole]:
		return cls.select_many(cur, {EmployeeRole.COLUMN_ROLE_ID: role_id})
	
	@classmethod
	def get_roles(cls, cur: psycopg.Cursor, employee_id: int) -> list[Role]:
		query = f"""
			SELECT r.*
			FROM roles r
			JOIN employee_roles er ON er.{EmployeeRole.COLUMN_ROLE_ID} = r.id
			JOIN employees e ON e.{Employee.COLUMN_ID} = er.{EmployeeRole.COLUMN_EMPLOYEE_ID}
			WHERE
				er.{EmployeeRole.COLUMN_EMPLOYEE_ID} = %s
				AND e.{Employee.COLUMN_FIRED_AT} IS NULL
				AND r.{Role.COLUMN_DEACTIVATED_AT} IS NULL
		"""

		cur.execute(query, (employee_id,))
		return [Role(**row) for row in cur.fetchall()]
