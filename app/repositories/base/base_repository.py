import psycopg
from typing import Any, ClassVar


class BaseRepository:
	TABLE: ClassVar[str]

	@staticmethod
	def execute_create(
		cur: psycopg.Cursor,
		table: str,
		fields: dict[str, Any],
		returning: str | list[str] | None = "id"
	) -> dict[str, Any]:
		if not fields:
			raise ValueError("`fields` is empty")

		keys = list(fields.keys())
		values = list(fields.values())
		columns = ", ".join(keys)
		placeholders = ", ".join(["%s"] * len(values))

		query = f"""
			INSERT INTO {table} ({columns})
			VALUES ({placeholders})
		"""
		if returning:
			returning_fields = [returning] if isinstance(returning, str) else returning
			query += " RETURNING " + ", ".join(returning_fields)

		cur.execute(query, values)
		if returning:
			row = cur.fetchone()
			if row is None:
				raise RuntimeError("INSERT ... RETURNING returned no rows")
			return row
		return None

	@staticmethod
	def execute_update(
		cur: psycopg.Cursor,
		table: str,
		where: dict[str, Any],
		fields: dict[str, Any]
	) -> int:
		if not where:
			raise ValueError("`where` is empty")
		if not fields:
			return 0

		set_parts = []
		params = []

		for key, value in fields.items():
			set_parts.append(f"{key} = %s")
			params.append(value)

		where_parts = []
		for key, value in where.items():
			where_parts.append(f"{key} = %s")
			params.append(value)

		query = f"""
			UPDATE {table}
			SET {", ".join(set_parts)}
			WHERE {" AND ".join(where_parts)}
		"""
		cur.execute(query, params)
		return cur.rowcount

	@staticmethod
	def execute_delete(
		cur: psycopg.Cursor,
		table: str,
		where: dict[str, Any]
	) -> int:
		if not where:
			raise ValueError("`where` is empty")
		
		where_parts = []
		params = []
		for key, value in where.items():
			where_parts.append(f"{key} = %s")
			params.append(value)

		query = f"""
			DELETE FROM {table}
			WHERE {" AND ".join(where_parts)}
		"""
		cur.execute(query, params)
		return cur.rowcount

	@staticmethod
	def execute_select(
		cur: psycopg.Cursor,
		table: str,
		where: dict[str, Any] | None = None,
		select_fields: list[str] | None = None,
		order_by: str | None = None,
		limit: int | None = None,
		offset: int | None = None
	) -> list[dict]:
		where = where or {}

		select_sql = ", ".join(select_fields) if select_fields else "*"
		where_parts = []
		params = []
		for key, value in where.items():
			where_parts.append(f"{key} = %s")
			params.append(value)

		query = f"SELECT {select_sql} FROM {table}"
		if where_parts:
			query += " WHERE " + " AND ".join(where_parts)
		if order_by:
			query += f" ORDER BY {order_by}"
		if limit is not None:
			query += " LIMIT %s"
			params.append(max(1, min(limit, 100)))
		if offset is not None:
			query += " OFFSET %s"
			params.append(max(0, offset))
		cur.execute(query, params)
		return cur.fetchall()
	
	@classmethod
	def execute_select_one(
		cls,
		cur: psycopg.Cursor,
		table: str,
		where: dict[str, Any] | None = None,
		select_fields: list[str] | None = None,
		order_by: str | None = None
	) -> dict | None:
		rows = cls.execute_select(
			cur=cur,
			table=table,
			where=where,
			select_fields=select_fields,
			order_by=order_by,
			limit=1 
		)

		return rows[0] if rows else None