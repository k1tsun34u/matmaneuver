import psycopg
from datetime import date
from typing import Any, Literal
from app.models.public.employee import Employee
from app.repositories.base_repository import BaseRepository


class EmployeesRepository(BaseRepository):
	TABLE = "employees"
	SELECT_FIELDS = [
		"id",
		"user_id",
		"hired_at",
		"fired_by",
		"fired_at",
		"created_by",
		"created_at"
	]

	@classmethod
	def create(
		cls,
		cur: psycopg.Cursor,
		user_id: int,
		hired_at: date,
		created_by: int | None
	) -> int:
		return cls.execute_create(
			cur=cur,
			table=cls.TABLE,
			fields={
				"user_id": user_id,
				"hired_at": hired_at,
				"created_by": created_by
			},
			returning="id"
		)["id"]
	
	@classmethod
	def fire(
		cls,
		cur: psycopg.Cursor,
		employee_id: int,
		fired_by: int
	) -> int:
		query = f"""
			UPDATE {cls.TABLE}
			SET fired_by = %s, fired_at = CURRENT_DATE
			WHERE id = %s AND fired_at IS NULL
		"""
		cur.execute(query, (fired_by, employee_id,))
		return cur.rowcount
	
	@classmethod
	def rehire(
		cls,
		cur: psycopg.Cursor,
		employee_id: int
	) -> int:
		query = f"""
			UPDATE {cls.TABLE}
			SET fired_by = NULL, fired_at = NULL
			WHERE id = %s AND fired_at IS NOT NULL
		"""
		cur.execute(query, (employee_id,))
		return cur.rowcount
	
	@classmethod
	def _get_by_property(
		cls,
		cur: psycopg.Cursor,
		field: Literal["id", "user_id"],
		value: Any,
		exclude_fired: bool = True
	) -> Employee | None:
		query = f"""
			SELECT {", ".join(cls.SELECT_FIELDS)}
			FROM {cls.TABLE}
			WHERE {field} = %s {'AND fired_at IS NULL' if exclude_fired else ''}
			LIMIT 1
		"""
		cur.execute(query, (value,))

		row = cur.fetchone()
		return Employee(**row) if row else None
	
	@classmethod
	def get_by_id(
		cls,
		cur: psycopg.Cursor,
		employee_id: int
	) -> Employee | None:
		return cls._get_by_property(cur, "id", employee_id)
	
	@classmethod
	def get_by_user_id(
		cls,
		cur: psycopg.Cursor,
		user_id: int
	) -> Employee | None:
		return cls._get_by_property(cur, "user_id", user_id)
	
	@classmethod
	def get_many(
		cls,
		cur: psycopg.Cursor,
		limit: int = 50,
		offset: int = 0,
		exclude_fired: bool = True
	) -> list[Employee]:
		limit, offset = cls.normalize_pagination(limit, offset)

		query = f"""
			SELECT {", ".join(cls.SELECT_FIELDS)}
			FROM {cls.TABLE}
			{'WHERE fired_at IS NULL' if exclude_fired else ''}
			ORDER BY created_at DESC
			LIMIT %s
			OFFSET %s
		"""
		cur.execute(query, (limit, offset,))
		return [Employee(**row) for row in cur.fetchall()]