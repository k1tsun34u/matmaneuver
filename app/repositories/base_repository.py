from typing import Any

import psycopg

from app.unset import Unset


class BaseRepository:
	@staticmethod
	def fetchone(cur: psycopg.Cursor, query: str, params: tuple = ()) -> dict | None:
		cur.execute(query, params)
		return cur.fetchone()

	@staticmethod
	def fetchall(cur: psycopg.Cursor, query: str, params: tuple = ()) -> list[dict]:
		cur.execute(query, params)
		return cur.fetchall()

	@staticmethod
	def execute(cur: psycopg.Cursor, query: str, params: tuple = ()) -> int:
		cur.execute(query, params)
		return cur.rowcount

	@staticmethod
	def normalize_pagination(limit: int, offset: int) -> tuple[int, int]:
		limit = max(1, min(limit, 100))
		offset = max(0, offset)
		return limit, offset

	@staticmethod
	def build_where(conditions: list[str]) -> str:
		return "WHERE " + " AND ".join(conditions) if conditions else ""

	@staticmethod
	def filter_unset(fields: dict[str, object]) -> dict[str, object]:
		return {k: v for k, v in fields.items() if not isinstance(v, Unset)}

	@staticmethod
	def ilike_any(fields: list[str], value: str) -> tuple[str, list]:
		condition = "(" + " OR ".join([f"{f} ILIKE %s" for f in fields]) + ")"
		params = [value] * len(fields)
		return condition, params

	# table must NEVER come from user input
	@staticmethod
	def execute_create(
		cur: psycopg.Cursor,
		table: str,
		fields: dict[str, object],
		# field_whitelist: set[str],
		returning: str | list[str] | None = "id",
	) -> dict[str, object]:
		if not fields:
			raise ValueError("`fields` is empty")

		# invalid_fields = set(fields) - field_whitelist
		# if invalid_fields:
		# 	raise ValueError(f"Invalid fields: {invalid_fields}")

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

	# table must NEVER come from user input
	@staticmethod
	def execute_update(
		cur: psycopg.Cursor,
		table: str,
		where: dict[str, object],
		# where_whitelist: set[str],
		fields: dict[str, object],
		# field_whitelist: set[str],
	) -> int:
		if not where:
			raise ValueError("`where` is empty")
		if not fields:
			return 0

		# invalid_where = set(where) - where_whitelist
		# if invalid_where:
		# 	raise ValueError(f"Invalid where fields: {invalid_where}")

		# invalid_fields = set(fields) - field_whitelist
		# if invalid_fields:
		# 	raise ValueError(f"Invalid update fields: {invalid_fields}")

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
		where: dict[str, object],
		# where_whitelist: set[str],
	) -> int:
		if not where:
			raise ValueError("`where` is empty")

		# invalid_where = set(where) - where_whitelist
		# if invalid_where:
		# 	raise ValueError(f"Invalid where fields: {invalid_where}")
		
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
		where: dict[str, object] | None = None,
		# where_whitelist: set[str] | None = None,
		select_fields: list[str] | None = None,
		order_by: str | None = None,
		limit: int | None = None,
		offset: int | None = None,
	) -> list[dict]:
		where = where or {}
		# if where_whitelist is not None:
		# 	invalid_where = set(where) - where_whitelist
		# 	if invalid_where:
		# 		raise ValueError(f"Invalid where fields: {invalid_where}")

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
		where: dict[str, object] | None = None,
		# where_whitelist: set[str] | None = None,
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