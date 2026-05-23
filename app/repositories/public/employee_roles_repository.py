import psycopg
from app.models.public.role import Role
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
		"employee_id",
		"role_id",
		"assigned_by",
		"assigned_at",
	)

	ORDER_BY = (("assigned_at", "DESC"),)

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
				"employee_id": employee_id,
				"role_id": role_id,
				"assigned_by": assigned_by
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
			"employee_id": employee_id,
			"role_id": role_id
		})
	
	@classmethod
	def assign_many(
		cls,
		cur: psycopg.Cursor,
		employee_id: int,
		role_ids: list[int],
		assigned_by: int | None
	) -> int:
		query = f"""
			INSERT INTO {cls.TABLE} ({", ".join(cls.SELECT_FIELDS)})
			SELECT
				%s,
				unnest(%s::bigint[]),
				%s,
				NOW()
			ON CONFLICT (employee_id, role_id) DO NOTHING
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
		query = f"""
			DELETE FROM {cls.TABLE} er
			USING (
				SELECT unnest(%s::bigint[]) AS role_id
			) r
			WHERE er.employee_id = %s AND er.role_id = r.role_id
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
		return cls.select(cur, {"employee_id": employee_id, "role_id": role_id})
	
	@classmethod
	def get_many_by_employee_id(cls, cur: psycopg.Cursor, employee_id: int) -> list[EmployeeRole]:
		return cls.select_many(cur, {"employee_id": employee_id})
	
	@classmethod
	def get_many_by_role_id(cls, cur: psycopg.Cursor, role_id: int) -> list[EmployeeRole]:
		return cls.select_many(cur, {"role_id": role_id})
	
	@classmethod
	def get_roles(cls, cur: psycopg.Cursor, employee_id: int) -> list[Role]:
		query = """
			SELECT r.*
			FROM roles r
			JOIN employee_roles er ON er.role_id = r.id
			WHERE er.employee_id = %s
		"""

		cur.execute(query, (employee_id,))
		return [Role(**row) for row in cur.fetchall()]
