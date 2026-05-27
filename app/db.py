import logging
from typing import Any
from psycopg.rows import dict_row
from contextlib import contextmanager
from psycopg_pool import ConnectionPool
from app.types.cart_type import CartType
import psycopg.types.enum as psycopg_enum
from app.types.order_status import OrderStatus
from app.types.supply_status import SupplyStatus
from app.types.payment_method import PaymentMethod
from app.types.write_off_reason import WriteOffReason


logger = logging.getLogger(__name__)

class Db:
	pool: ConnectionPool | None = None

	@classmethod
	def init(cls, host, port, db_name, user):
		conninfo = (
			f"dbname={db_name} "
			f"user={user} "
			f"host={host} "
			f"port={port} "
			f"connect_timeout=5"
		)

		cls.pool = ConnectionPool(
			conninfo=conninfo,
			min_size=5,
			max_size=20,
			open=True,
			kwargs={"row_factory": dict_row},
		)

		with cls.connection():
			cls.register_enums()
	
	@classmethod
	def register_enums(cls):
		Db.register_enum("supply_status", SupplyStatus)
		Db.register_enum("order_status", OrderStatus)
		Db.register_enum("write_off_reason", WriteOffReason)
		Db.register_enum("payment_method", PaymentMethod)
		Db.register_enum("cart_type", CartType)

	@classmethod
	def close(cls):
		if cls.pool: cls.pool.close()

	@classmethod
	def _ensure_pool(cls):
		if not cls.pool: raise RuntimeError("Database pool is not initialized")
		
	@classmethod
	@contextmanager
	def connection(cls):
		cls._ensure_pool()
		with cls.pool.connection() as conn:
			yield conn
	
	@classmethod
	def register_enum(
		cls,
		name: str,
		enum: Any
	):
		with cls.connection() as conn:
			info = psycopg_enum.EnumInfo.fetch(conn, name)
			psycopg_enum.register_enum(info, conn, enum)
