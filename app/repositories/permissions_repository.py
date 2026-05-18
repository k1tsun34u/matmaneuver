import psycopg
from typing import Any, Literal
from app.models.public.permission import Permission
from app.repositories.base_repository import BaseRepository


class PermissionsRepository(BaseRepository):
	TABLE = "permissions"
	SELECT_FIELDS = [
		"id",
		"code",
		"description",
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
		description: str | None,
		created_by: int | None
	) -> int:
		return cls.execute_create(
			cur=cur,
			table=cls.TABLE,
			fields={
				"code": code,
				"description": description,
				"is_system": False,
				"created_by": created_by
			},
			returning="id"
		)["id"]
	
	@classmethod
	def set_description(
		cls,
		cur: psycopg.Cursor,
		permission_id: int,
		description: str | None
	) -> int:
		return cls.execute_update(
			cur=cur,
			table=cls.TABLE,
			where={"id": permission_id},
			fields={"description": description}
		)
	
	@classmethod
	def deactivate(
		cls,
		cur: psycopg.Cursor,
		permission_id: int,
		deactivated_by: int
	) -> int:
		query = f"""
			UPDATE {cls.TABLE}
			SET deactivated_by = %s, deactivated_at = NOW()
			WHERE id = %s AND is_system = FALSE AND deactivated_at IS NULL
		"""
		cur.execute(query, (deactivated_by, permission_id,))
		return cur.rowcount
	
	@classmethod
	def restore(
		cls,
		cur: psycopg.Cursor,
		permission_id: int
	) -> int:
		query = f"""
			UPDATE {cls.TABLE}
			SET deactivated_by = NULL, deactivated_at = NULL
			WHERE id = %s AND is_system = FALSE AND deactivated_at IS NOT NULL
		"""
		cur.execute(query, (permission_id,))
		return cur.rowcount
	
	@classmethod
	def _get_by_property(
		cls,
		cur: psycopg.Cursor,
		field: Literal["id", "code"],
		value: Any,
		exclude_deactivated: bool = True
	) -> Permission | None:
		query = f"""
			SELECT {", ".join(cls.SELECT_FIELDS)}
			FROM {cls.TABLE}
			WHERE {field} = %s {'AND deactivated_at IS NULL' if exclude_deactivated else ''}
			LIMIT 1
		"""
		cur.execute(query, (value,))

		row = cur.fetchone()
		return Permission(**row) if row else None
	
	@classmethod
	def get_by_id(
		cls,
		cur: psycopg.Cursor,
		permission_id: int,
		exclude_deactivated: bool = True
	) -> Permission | None:
		return cls._get_by_property(cur, "id", permission_id, exclude_deactivated)
	
	@classmethod
	def get_by_code(
		cls,
		cur: psycopg.Cursor,
		code: str,
		exclude_deactivated: bool = True
	) -> Permission | None:
		return cls._get_by_property(cur, "code", code, exclude_deactivated)
	
	@classmethod
	def get_many(
		cls,
		cur: psycopg.Cursor,
		limit: int = 50,
		offset: int = 0,
		exclude_deactivated: bool = True
	) -> list[Permission]:
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
		return [Permission(**row) for row in cur.fetchall()]