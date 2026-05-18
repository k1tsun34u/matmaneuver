import psycopg
from typing import Any, Literal
from app.models.public.employee_role import EmployeeRole
from app.repositories.base_repository import BaseRepository


class EmployeeRolesRepository(BaseRepository):
	TABLE = "employee_roles"
	SELECT_FIELDS = [
		"employee_id",
		"role_id",
		"assigned_by",
		"assigned_at"
	]

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
		cur.execute(query, (employee_id, role_ids,))
		return cur.rowcount
	
	@classmethod
	def get_by_employee_id_role_id(
		cls,
		cur: psycopg.Cursor,
		employee_id: int,
		role_id: int
	) -> EmployeeRole | None:
		row = cls.execute_select_one(
			cur=cur,
			table=cls.TABLE,
			where={"employee_id": employee_id, "role_id": role_id}
		)

		return EmployeeRole(**row) if row else None
	
	@classmethod
	def _get_many_by_property(
		cls,
		cur: psycopg.Cursor,
		field: Literal["employee_id", "role_id"],
		value: Any
	) -> list[EmployeeRole]:
		rows = cls.execute_select(
			cur=cur,
			table=cls.TABLE,
			where={field: value}
		)

		return [EmployeeRole(**row) for row in rows]
	
	@classmethod
	def get_many_by_employee_id(
		cls,
		cur: psycopg.Cursor,
		employee_id: int
	) -> list[EmployeeRole]:
		return cls._get_many_by_property(cur, "employee_id", employee_id)
	
	@classmethod
	def get_many_by_role_id(
		cls,
		cur: psycopg.Cursor,
		role_id: int
	) -> list[EmployeeRole]:
		return cls._get_many_by_property(cur, "role_id", role_id)