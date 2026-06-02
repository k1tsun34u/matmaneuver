import psycopg
from app.dtos.api.employee.response_complete_warehouse_product import ResponseCompleteWarehouseProduct
from app.models.public.warehouse import Warehouse
from app.utils import Utils
from typing import ClassVar
from typing import TypeVar
from app.types.delete_result import DeleteResult
from app.types.update_result import UpdateResult
from app.models.public.warehouse_product import WarehouseProduct
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.updatable_mixin import UpdatableMixin
from app.repositories.base.mixins.selectable_mixin import SelectableMixin


T = TypeVar("T")

class WarehouseProductsRepository(
	BaseRepository,
	UpdatableMixin,
	SelectableMixin[WarehouseProduct]
):
	TABLE: ClassVar[str] = WarehouseProduct.TABLE
	MODEL = WarehouseProduct
	TABLE_COLUMNS = (
		WarehouseProduct.COLUMN_PRODUCT_ID,
		WarehouseProduct.COLUMN_WAREHOUSE_ID,
		WarehouseProduct.COLUMN_QUANTITY,
		WarehouseProduct.COLUMN_RESERVED_QUANTITY,
		WarehouseProduct.COLUMN_CREATED_BY,
		WarehouseProduct.COLUMN_CREATED_AT,
	)

	ORDER_BY = ((WarehouseProduct.COLUMN_CREATED_AT, "DESC",),)

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
			table=WarehouseProduct.TABLE,
			fields={
				WarehouseProduct.COLUMN_PRODUCT_ID: product_id,
				WarehouseProduct.COLUMN_WAREHOUSE_ID: warehouse_id,
				WarehouseProduct.COLUMN_CREATED_BY: created_by
			},
			returning=None
		)
	
	@classmethod
	def delete(cls, cur: psycopg.Cursor, product_id: int, warehouse_id: int) -> DeleteResult:
		rowcount = cls.execute_delete(cur, WarehouseProduct.TABLE, {
			WarehouseProduct.COLUMN_PRODUCT_ID: product_id,
			WarehouseProduct.COLUMN_WAREHOUSE_ID: warehouse_id,
			WarehouseProduct.COLUMN_QUANTITY: 0,
			WarehouseProduct.COLUMN_RESERVED_QUANTITY: 0
		})
		
		return Utils.determine_result(
			cur=cur,
			table=cls.TABLE,
			where={
				WarehouseProduct.COLUMN_PRODUCT_ID: product_id,
				WarehouseProduct.COLUMN_WAREHOUSE_ID: warehouse_id
			},
			rowcount=rowcount,
			result_type=DeleteResult
		)
	
	@classmethod
	def delete_many_by_product_id(cls, cur: psycopg.Cursor, product_id: int) -> DeleteResult:
		rowcount = cls.execute_delete(cur, WarehouseProduct.TABLE, {
			WarehouseProduct.COLUMN_PRODUCT_ID: product_id,
			WarehouseProduct.COLUMN_QUANTITY: 0,
			WarehouseProduct.COLUMN_RESERVED_QUANTITY: 0
		})
		
		return Utils.determine_result(
			cur=cur,
			table=cls.TABLE,
			where={WarehouseProduct.COLUMN_PRODUCT_ID: product_id},
			rowcount=rowcount,
			result_type=DeleteResult
		)
	
	@classmethod
	def delete_many_by_warehouse_id(cls, cur: psycopg.Cursor, warehouse_id: int) -> DeleteResult:
		rowcount = cls.execute_delete(cur, WarehouseProduct.TABLE, {
			WarehouseProduct.COLUMN_WAREHOUSE_ID: warehouse_id,
			WarehouseProduct.COLUMN_QUANTITY: 0,
			WarehouseProduct.COLUMN_RESERVED_QUANTITY: 0
		})
		
		return Utils.determine_result(
			cur=cur,
			table=cls.TABLE,
			where={WarehouseProduct.COLUMN_WAREHOUSE_ID: warehouse_id},
			rowcount=rowcount,
			result_type=DeleteResult
		)
	
	@classmethod
	def increase_quantity(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		warehouse_id: int,
		quantity: int
	) -> UpdateResult:
		if quantity <= 0:
			return UpdateResult.FAIL_CONDITION
		
		query = f"""
			UPDATE {WarehouseProduct.TABLE}
			SET {WarehouseProduct.COLUMN_QUANTITY} = {WarehouseProduct.COLUMN_QUANTITY} + %s
			WHERE
				{WarehouseProduct.COLUMN_PRODUCT_ID} = %s
				AND {WarehouseProduct.COLUMN_WAREHOUSE_ID} = %s
		"""
		cur.execute(query, (quantity, product_id, warehouse_id,))

		return Utils.determine_result(
			cur=cur,
			table=cls.TABLE,
			where={
				WarehouseProduct.COLUMN_PRODUCT_ID: product_id,
				WarehouseProduct.COLUMN_WAREHOUSE_ID: warehouse_id
			}, 
			rowcount=cur.rowcount,
			result_type=UpdateResult
		)
	
	@classmethod
	def decrease_quantity(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		warehouse_id: int,
		quantity: int
	) -> UpdateResult:
		if quantity <= 0:
			return UpdateResult.FAIL_CONDITION

		query = f"""
			UPDATE {WarehouseProduct.TABLE}
			SET {WarehouseProduct.COLUMN_QUANTITY} = {WarehouseProduct.COLUMN_QUANTITY} - %s
			WHERE
				{WarehouseProduct.COLUMN_PRODUCT_ID} = %s
				AND {WarehouseProduct.COLUMN_WAREHOUSE_ID} = %s
				AND {WarehouseProduct.COLUMN_QUANTITY} >= %s
				AND ({WarehouseProduct.COLUMN_QUANTITY} - %s) >= {WarehouseProduct.COLUMN_RESERVED_QUANTITY}
		"""
		cur.execute(query, (quantity, product_id, warehouse_id, quantity, quantity,))

		return Utils.determine_result(
			cur=cur,
			table=cls.TABLE,
			where={
				WarehouseProduct.COLUMN_PRODUCT_ID: product_id,
				WarehouseProduct.COLUMN_WAREHOUSE_ID: warehouse_id
			},
			rowcount=cur.rowcount,
			result_type=UpdateResult
		)
	
	@classmethod
	def reserve(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		warehouse_id: int,
		reserve_quantity: int
	) -> UpdateResult:
		if reserve_quantity <= 0:
			return UpdateResult.FAIL_CONDITION

		query = f"""
			UPDATE {WarehouseProduct.TABLE}
			SET {WarehouseProduct.COLUMN_RESERVED_QUANTITY} = {WarehouseProduct.COLUMN_RESERVED_QUANTITY} + %s
			WHERE
				{WarehouseProduct.COLUMN_PRODUCT_ID} = %s
				AND {WarehouseProduct.COLUMN_WAREHOUSE_ID} = %s
				AND ({WarehouseProduct.COLUMN_RESERVED_QUANTITY} + %s) <= {WarehouseProduct.COLUMN_QUANTITY}
		"""
		cur.execute(query, (reserve_quantity, product_id, warehouse_id, reserve_quantity,))

		return Utils.determine_result(
			cur=cur,
			table=cls.TABLE,
			where={
				WarehouseProduct.COLUMN_PRODUCT_ID: product_id,
				WarehouseProduct.COLUMN_WAREHOUSE_ID: warehouse_id
			},
			rowcount=cur.rowcount,
			result_type=UpdateResult
		)
	
	@classmethod
	def unreserve(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		warehouse_id: int,
		reserve_quantity: int
	) -> UpdateResult:
		if reserve_quantity <= 0:
			return UpdateResult.FAIL_CONDITION

		query = f"""
			UPDATE {WarehouseProduct.TABLE}
			SET {WarehouseProduct.COLUMN_RESERVED_QUANTITY} = {WarehouseProduct.COLUMN_RESERVED_QUANTITY} - %s
			WHERE
				{WarehouseProduct.COLUMN_PRODUCT_ID} = %s
				AND {WarehouseProduct.COLUMN_WAREHOUSE_ID} = %s
				AND {WarehouseProduct.COLUMN_RESERVED_QUANTITY} >= %s
		"""
		cur.execute(query, (reserve_quantity, product_id, warehouse_id, reserve_quantity,))

		return Utils.determine_result(
			cur=cur,
			table=cls.TABLE,
			where={
				WarehouseProduct.COLUMN_PRODUCT_ID: product_id,
				WarehouseProduct.COLUMN_WAREHOUSE_ID: warehouse_id
			}, 
			rowcount=cur.rowcount,
			result_type=UpdateResult
		)
	
	@classmethod
	def consume(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		warehouse_id: int,
		quantity: int
	) -> UpdateResult:
		if quantity <= 0:
			return UpdateResult.FAIL_CONDITION
		
		query = f"""
			UPDATE {WarehouseProduct.TABLE}
			SET
				{WarehouseProduct.COLUMN_QUANTITY} = {WarehouseProduct.COLUMN_QUANTITY} - %s,
				{WarehouseProduct.COLUMN_RESERVED_QUANTITY} = {WarehouseProduct.COLUMN_RESERVED_QUANTITY} - %s
			WHERE
				{WarehouseProduct.COLUMN_PRODUCT_ID} = %s
				AND {WarehouseProduct.COLUMN_WAREHOUSE_ID} = %s
				AND {WarehouseProduct.COLUMN_RESERVED_QUANTITY} >= %s
				AND {WarehouseProduct.COLUMN_QUANTITY} >= %s
		"""
		cur.execute(query, (
			quantity, quantity,
			product_id, warehouse_id,
			quantity, quantity,
		))

		return Utils.determine_result(
			cur=cur,
			table=cls.TABLE,
			where={
				WarehouseProduct.COLUMN_PRODUCT_ID: product_id,
				WarehouseProduct.COLUMN_WAREHOUSE_ID: warehouse_id
			},
			rowcount=cur.rowcount,
			result_type=UpdateResult
		)
	
	@classmethod
	def get_by_product_id_warehouse_id(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		warehouse_id: int
	) -> WarehouseProduct | None:
		return cls.select(
			cur=cur,
			equals={
				WarehouseProduct.COLUMN_PRODUCT_ID: product_id,
				WarehouseProduct.COLUMN_WAREHOUSE_ID: warehouse_id
			}
		)
	
	@classmethod
	def get_many_by_product_id(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		limit: int = 50,
		offset: int = 0
	) -> tuple[list[WarehouseProduct], int]:
		products = cls.select_many(
			cur=cur,
			equals={WarehouseProduct.COLUMN_PRODUCT_ID: product_id},
			limit=limit,
			offset=offset
		)

		query = f"""
			SELECT COUNT(*) AS total
			FROM {cls.TABLE}
			WHERE {WarehouseProduct.COLUMN_PRODUCT_ID} = %s
		"""
		cur.execute(query, (product_id,))
		return (products, cur.fetchone()['total'],)
	
	@classmethod
	def get_many_by_warehouse_id(
		cls,
		cur: psycopg.Cursor,
		warehouse_id: int,
		limit: int = 50,
		offset: int = 0
	) -> tuple[list[WarehouseProduct], int]:
		products = cls.select_many(
			cur=cur,
			equals={WarehouseProduct.COLUMN_WAREHOUSE_ID: warehouse_id},
			limit=limit,
			offset=offset
		)

		query = f"""
			SELECT COUNT(*) AS total
			FROM {cls.TABLE}
			WHERE {WarehouseProduct.COLUMN_WAREHOUSE_ID} = %s
		"""
		cur.execute(query, (warehouse_id,))
		return (products, cur.fetchone()['total'],)
	
	@classmethod
	def get_complete_warehouse_products_by_product_id(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		exclude_deleted: bool = True,
		limit: int = 50,
		offset: int = 0
	) -> tuple[list[ResponseCompleteWarehouseProduct], int]:
		conditions, params = Utils.build_conditions_params(
			equals={f"wp.{WarehouseProduct.COLUMN_PRODUCT_ID}": product_id},
			is_null=(f"w.{Warehouse.COLUMN_DELETED_AT}",) if exclude_deleted else None
		)

		query_part = f"""
			FROM {Warehouse.TABLE} w
			JOIN {WarehouseProduct.TABLE} wp ON w.{Warehouse.COLUMN_ID} = wp.{WarehouseProduct.COLUMN_WAREHOUSE_ID}
			{Utils.build_where(conditions)}
		"""

		query = f"""
			SELECT
				w*,
				wp*
			{query_part}
			{Utils.build_order_by(cls.ORDER_BY)}
			LIMIT %s
			OFFSET %s
		"""
		cur.execute(query, params + (limit, offset,))
		complete_warehouse_products = [ResponseCompleteWarehouseProduct(**row) for row in cur.fetchall()]

		query = f"""
			SELECT COUNT(*) AS total
			{query_part}
		"""
		cur.execute(query, params)
		return (complete_warehouse_products, cur.fetchone()['total'],)
