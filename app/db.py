import logging
from typing import Any

from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

logger = logging.getLogger(__name__)

class Db:
	pool: ConnectionPool | None = None

	@classmethod
	def init(cls, host, port, db_name, user):
		cls.pool = ConnectionPool(
			conninfo=(
				f"dbname={db_name} "
				f"user={user} "
				f"host={host} "
				f"port={port} "
				f"connect_timeout=5"
			),
			min_size=1,
			max_size=10,
			open=True,
			kwargs={"row_factory": dict_row},
		)

	@classmethod
	def close(cls):
		if cls.pool: cls.pool.close()

	@classmethod
	def _ensure_pool(cls):
		if not cls.pool: raise RuntimeError("Database pool is not initialized")
		
	@classmethod
	def connection(cls):
		cls._ensure_pool()
		
		return cls.pool.connection()

	@classmethod
	def fetchone(cls, query, params=None) -> dict[str, Any] | None:
		cls._ensure_pool()

		try:
			with cls.pool.connection() as con:
				with con.cursor() as cur:
					cur.execute(query, params)
					return cur.fetchone()
		except Exception:
			logger.exception("Database error")
			raise

	@classmethod
	def fetchall(cls, query, params=None) -> list[dict[str, Any]]:
		cls._ensure_pool()

		try:
			with cls.pool.connection() as con:
				with con.cursor() as cur:
					cur.execute(query, params)
					return cur.fetchall()
		except Exception:
			logger.exception("Database error")
			raise

	@classmethod
	def execute(cls, query, params=None) -> int:
		cls._ensure_pool()

		try:
			with cls.pool.connection() as con:
				with con.cursor() as cur:
					cur.execute(query, params)
					return cur.rowcount
		except Exception:
			logger.exception("Database error")
			raise