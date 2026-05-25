import psycopg
from app.utils import Utils
from typing import ClassVar
from typing import TypeVar
from app.types.delete_result import DeleteResult
from app.types.update_result import UpdateResult
from app.models.public.warehouse_product import WarehouseProduct
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.deletable_mixin import DeletableMixin
from app.repositories.base.mixins.updatable_mixin import UpdatableMixin
from app.repositories.base.mixins.selectable_mixin import SelectableMixin


T = TypeVar("T")

class WarehouseProductsRepository(
	BaseRepository,
	UpdatableMixin,
	DeletableMixin,
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
	def get_many_by_product_id(cls, cur: psycopg.Cursor, product_id: int) -> list[WarehouseProduct]:
		return cls.select_many(
			cur=cur,
			equals={WarehouseProduct.COLUMN_PRODUCT_ID: product_id}
		)
	
	@classmethod
	def get_many_by_warehouse_id(cls, cur: psycopg.Cursor, warehouse_id: int) -> list[WarehouseProduct]:
		return cls.select_many(
			cur=cur,
			equals={WarehouseProduct.COLUMN_WAREHOUSE_ID: warehouse_id}
		)
