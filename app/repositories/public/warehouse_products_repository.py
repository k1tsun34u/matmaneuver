import psycopg
from app.models.public.warehouse_product import WarehouseProduct
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.selectable_mixin import SelectableMixin


class WarehouseProductsRepository(
	BaseRepository,
	SelectableMixin[WarehouseProduct]
):
	TABLE = "warehouse_products"
	MODEL = WarehouseProduct
	TABLE_COLUMNS = (
		"product_id",
		"warehouse_id",
		"quantity",
		"reserved_quantity",
		"created_by",
		"created_at",
	)

	ORDER_BY = (("created_at", "DESC"),)

	@classmethod
	def create(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		warehouse_id: int,
		created_by: int | None
	) -> None:
		cls.execute_create(
			cur=cur,
			table=cls.TABLE,
			fields={
				"product_id": product_id,
				"warehouse_id": warehouse_id,
				"created_by": created_by
			},
			returning=None
		)
	
	@classmethod
	def delete(cls, cur: psycopg.Cursor, product_id: int, warehouse_id: int) -> int:
		return cls.execute_delete(cur, cls.TABLE, {
			"product_id": product_id,
			"warehouse_id": warehouse_id,
			"quantity": 0,
			"reserved_quantity": 0
		})
	
	@classmethod
	def delete_many_by_product_id(cls, cur: psycopg.Cursor, product_id: int) -> int:
		return cls.execute_delete(cur, cls.TABLE, {
			"product_id": product_id,
			"quantity": 0,
			"reserved_quantity": 0
		})
	
	@classmethod
	def delete_many_by_warehouse_id(cls, cur: psycopg.Cursor, warehouse_id: int) -> int:
		return cls.execute_delete(cur, cls.TABLE, {
			"warehouse_id": warehouse_id,
			"quantity": 0,
			"reserved_quantity": 0
		})
	
	@classmethod
	def increase_quantity(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		warehouse_id: int,
		quantity: int
	) -> int:
		if quantity <= 0:
			raise ValueError("`quantity` must be > 0")
		
		query = f"""
			UPDATE {cls.TABLE}
			SET quantity = quantity + %s
			WHERE product_id = %s AND warehouse_id = %s
		"""
		cur.execute(query, (quantity, product_id, warehouse_id,))
		return cur.rowcount
	
	@classmethod
	def decrease_quantity(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		warehouse_id: int,
		quantity: int
	) -> int:
		if quantity <= 0:
			raise ValueError("`quantity` must be > 0")

		query = f"""
			UPDATE {cls.TABLE}
			SET quantity = quantity - %s
			WHERE
				product_id = %s AND warehouse_id = %s
				AND quantity >= %s
				AND (quantity - %s) >= reserved_quantity
		"""
		cur.execute(query, (quantity, product_id, warehouse_id, quantity, quantity,))
		return cur.rowcount
	
	@classmethod
	def reserve(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		warehouse_id: int,
		reserve_quantity: int
	) -> int:
		if reserve_quantity <= 0:
			raise ValueError("`reserve_quantity` must be > 0")

		query = f"""
			UPDATE {cls.TABLE}
			SET reserved_quantity = reserved_quantity + %s
			WHERE
				product_id = %s AND warehouse_id = %s
				AND (reserved_quantity + %s) <= quantity
		"""
		cur.execute(query, (reserve_quantity, product_id, warehouse_id, reserve_quantity,))
		return cur.rowcount
	
	@classmethod
	def unreserve(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		warehouse_id: int,
		reserve_quantity: int
	) -> int:
		if reserve_quantity <= 0:
			raise ValueError("`reserve_quantity` must be > 0")

		query = f"""
			UPDATE {cls.TABLE}
			SET reserved_quantity = reserved_quantity - %s
			WHERE
				product_id = %s AND warehouse_id = %s
				AND reserved_quantity >= %s
		"""
		cur.execute(query, (reserve_quantity, product_id, warehouse_id, reserve_quantity,))
		return cur.rowcount
	
	@classmethod
	def consume(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		warehouse_id: int,
		quantity: int
	) -> int:
		if quantity <= 0:
			raise ValueError("`quantity` must be > 0")
		
		query = f"""
			UPDATE {cls.TABLE}
			SET
				quantity = quantity - %s,
				reserved_quantity = reserved_quantity - %s
			WHERE
				product_id = %s AND warehouse_id = %s
				AND reserved_quantity >= %s
				AND quantity >= %s
		"""
		cur.execute(query, (
			quantity, quantity,
			product_id, warehouse_id,
			quantity, quantity,
		))
		return cur.rowcount
	
	@classmethod
	def get_by_product_id_warehouse_id(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		warehouse_id: int
	) -> WarehouseProduct | None:
		return cls.select(cur, {"product_id": product_id, "warehouse_id": warehouse_id})
	
	@classmethod
	def get_many_by_product_id(cls, cur: psycopg.Cursor, product_id: int) -> list[WarehouseProduct]:
		return cls.select_many(cur, {"product_id": product_id})
	
	@classmethod
	def get_many_by_warehouse_id(cls, cur: psycopg.Cursor, warehouse_id: int) -> list[WarehouseProduct]:
		return cls.select_many(cur, {"warehouse_id": warehouse_id})