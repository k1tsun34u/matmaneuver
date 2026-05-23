import psycopg
from app.models.public.role import Role
from app.models.public.employee import Employee
from app.models.public.employee_role import EmployeeRole
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.selectable_mixin import SelectableMixin


class EmployeeRolesRepository(
	BaseRepository,
	SelectableMixin[EmployeeRole]
):
	TABLE = "employee_roles"
	MODEL = EmployeeRole
	SELECT_FIELDS = (
		EmployeeRole.COLUMN_EMPLOYEE_ID,
		EmployeeRole.COLUMN_ROLE_ID,
		EmployeeRole.COLUMN_ASSIGNED_BY,
		EmployeeRole.COLUMN_ASSIGNED_AT,
	)

	ORDER_BY = ((EmployeeRole.COLUMN_ASSIGNED_AT, "DESC"),)

	@classmethod
	def assign(
		cls,
		cur: psycopg.Cursor,
		employee_id: int,
		role_id: int,
		assigned_by: int | None
	) -> None:
		cls.execute_create(
			cur=cur,
			table=cls.TABLE,
			fields={
				EmployeeRole.COLUMN_EMPLOYEE_ID: employee_id,
				EmployeeRole.COLUMN_ROLE_ID: role_id,
				EmployeeRole.COLUMN_ASSIGNED_BY: assigned_by
			},
			returning=None
		)
	
	@classmethod
	def unassign(
		cls,
		cur: psycopg.Cursor,
		employee_id: int,
		role_id: int
	) -> int:
		return cls.execute_delete(cur, cls.TABLE, {
			EmployeeRole.COLUMN_EMPLOYEE_ID: employee_id,
			EmployeeRole.COLUMN_ROLE_ID: role_id
		})
	
	@classmethod
	def assign_many(
		cls,
		cur: psycopg.Cursor,
		employee_id: int,
		role_ids: list[int],
		assigned_by: int | None
	) -> int:
		if not role_ids:
			return 0

		role_ids = list(dict.fromkeys(role_ids))
		query = f"""
			INSERT INTO {cls.TABLE} ({", ".join(cls.SELECT_FIELDS)})
			SELECT
				%s,
				unnest(%s::bigint[]),
				%s,
				NOW()
			ON CONFLICT ({EmployeeRole.COLUMN_EMPLOYEE_ID}, {EmployeeRole.COLUMN_ROLE_ID}) DO NOTHING
		"""
		cur.execute(query, (employee_id, role_ids, assigned_by,))
		return cur.rowcount
	
	@classmethod
	def unassign_many(
		cls,
		cur: psycopg.Cursor,
		employee_id: int,
		role_ids: list[int]
	) -> int:
		if not role_ids:
			return 0

		role_ids = list(dict.fromkeys(role_ids))
		query = f"""
			DELETE FROM {cls.TABLE} er
			USING (
				SELECT unnest(%s::bigint[]) AS {EmployeeRole.COLUMN_ROLE_ID}
			) r
			WHERE er.{EmployeeRole.COLUMN_EMPLOYEE_ID} = %s AND er.{EmployeeRole.COLUMN_ROLE_ID} = r.{EmployeeRole.COLUMN_ROLE_ID}
		"""
		cur.execute(query, (role_ids, employee_id,))
		return cur.rowcount
	
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
