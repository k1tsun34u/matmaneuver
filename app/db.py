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
			configure=cls.configure_connection
		)

	@classmethod
	def configure_connection(cls, conn):
		print(f"🔧 Configuring connection: {id(conn)}")
		conn.row_factory = dict_row
		cls.register_enums(conn)
	
	@classmethod
	def register_enums(cls, conn):
		cls.register_enum(conn, "supply_status", SupplyStatus)
		cls.register_enum(conn, "order_status", OrderStatus)
		cls.register_enum(conn, "write_off_reason", WriteOffReason)
		cls.register_enum(conn, "payment_method", PaymentMethod)
		cls.register_enum(conn, "cart_type", CartType)

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
		conn,
		name: str,
		enum: Any
	):
		try:
			mapping = {member.name: member.value for member in enum}

			info = psycopg_enum.EnumInfo.fetch(conn, name)
			psycopg_enum.register_enum(info, conn, enum=enum, mapping=mapping)
			print(f"✅ Registered {name} -> {enum.__name__}")
		except Exception as e:
			print(f"❌ Failed to register {name}: {e}")
