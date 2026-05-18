import psycopg
from typing import Any, Literal
from app.models.public.role import Role
from app.repositories.base_repository import BaseRepository


class RolesRepository(BaseRepository):
	TABLE = "roles"
	SELECT_FIELDS = [
		"id",
		"code",
		"is_system",
		"deactivated_by",
		"deactivated_at",
		"created_by",
		"created_at"
	]

	@classmethod
	def create(
		cls,
		cur: psycopg.Cursor,
		code: str,
		created_by: int | None
	) -> int:
		return cls.execute_create(
			cur=cur,
			table=cls.TABLE,
			fields={
				"code": code,
				"is_system": False,
				"created_by": created_by
			},
			returning="id"
		)["id"]
	
	@classmethod
	def deactivate(
		cls,
		cur: psycopg.Cursor,
		role_id: int,
		deactivated_by: int
	) -> int:
		query = f"""
			UPDATE {cls.TABLE}
			SET deactivated_by = %s, deactivated_at = NOW()
			WHERE id = %s AND is_system = FALSE AND deactivated_at IS NULL
		"""
		cur.execute(query, (deactivated_by, role_id,))
		return cur.rowcount
	
	@classmethod
	def restore(
		cls,
		cur: psycopg.Cursor,
		role_id: int
	) -> int:
		query = f"""
			UPDATE {cls.TABLE}
			SET deactivated_by = NULL, deactivated_at = NULL
			WHERE id = %s AND is_system = FALSE AND deactivated_at IS NOT NULL
		"""
		cur.execute(query, (role_id,))
		return cur.rowcount
	
	@classmethod
	def _get_by_property(
		cls,
		cur: psycopg.Cursor,
		field: Literal["id", "code"],
		value: Any,
		exclude_deactivated: bool = True
	) -> Role | None:
		query = f"""
			SELECT {", ".join(cls.SELECT_FIELDS)}
			FROM {cls.TABLE}
			WHERE {field} = %s {'AND deactivated_at IS NULL' if exclude_deactivated else ''}
			LIMIT 1
		"""
		cur.execute(query, (value,))

		row = cur.fetchone()
		return Role(**row) if row else None
	
	@classmethod
	def get_by_id(
		cls,
		cur: psycopg.Cursor,
		role_id: int,
		exclude_deactivated: bool = True
	) -> Role | None:
		return cls._get_by_property(cur, "id", role_id, exclude_deactivated)
	
	@classmethod
	def get_by_code(
		cls,
		cur: psycopg.Cursor,
		code: str,
		exclude_deactivated: bool = True
	) -> Role | None:
		return cls._get_by_property(cur, "code", code, exclude_deactivated)
	
	@classmethod
	def get_many(
		cls,
		cur: psycopg.Cursor,
		limit: int = 50,
		offset: int = 0,
		exclude_deactivated: bool = True
	) -> list[Role]:
		limit, offset = cls.normalize_pagination(limit, offset)

		query = f"""
			SELECT {", ".join(cls.SELECT_FIELDS)}
			FROM {cls.TABLE}
			{'WHERE deactivated_at IS NULL' if exclude_deactivated else ''}
			ORDER BY created_at DESC
			LIMIT %s
			OFFSET %s
		"""
		cur.execute(query, (limit, offset,))
		return [Role(**row) for row in cur.fetchall()]