import logging
from typing import Any
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool
import psycopg.types.enum as psycopg_enum
from app.types.order_status import OrderStatus
from app.types.return_status import ReturnStatus
from app.types.supply_status import SupplyStatus

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
			configure=Db._on_connect,
			kwargs={"row_factory": dict_row},
		)
	
	
	@staticmethod
	def _on_connect(_):
		Db.register_enum("supply_status", SupplyStatus)
		Db.register_enum("order_status", OrderStatus)
		Db.register_enum("return_status", ReturnStatus)

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
	
	@classmethod
	def register_enum(
		cls,
		name: str,
		enum: Any
	):
		with cls.connection() as conn:
			info = psycopg_enum.EnumInfo.fetch(conn, name)
			psycopg_enum.register_enum(info, conn, enum)
