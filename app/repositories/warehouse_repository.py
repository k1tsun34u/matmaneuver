import psycopg
from typing import Any, Literal
from app.models.public.warehouse import Warehouse
from app.repositories.base_repository import BaseRepository


class WarehouseRepository(BaseRepository):
	TABLE = "warehouses"
	SELECT_FIELDS = [
		"id",
		"address",
		"description",
		"deleted_by",
		"deleted_at",
		"created_by",
		"created_at"
	]

	@classmethod
	def create(
		cls,
		cur: psycopg.Cursor,
		address: str,
		description: str | None,
		created_by: int | None
	) -> int:
		return cls.execute_create(
			cur=cur,
			table=cls.TABLE,
			fields={
				"address": address,
				"description": description,
				"created_by": created_by
			},
			returning="id"
		)["id"]
	
	@classmethod
	def soft_delete(
		cls,
		cur: psycopg.Cursor,
		warehouse_id: int,
		deleted_by: int
	) -> int:
		query = f"""
			UPDATE {cls.TABLE}
			SET deleted_by = %s, deleted_at = NOW()
			WHERE id = %s AND deleted_at IS NULL
		"""
		cur.execute(query, (deleted_by, warehouse_id,))
		return cur.rowcount
	
	@classmethod
	def restore(
		cls,
		cur: psycopg.Cursor,
		warehouse_id: int
	) -> int:
		query = f"""
			UPDATE {cls.TABLE}
			SET deleted_by = NULL, deleted_at = NULL
			WHERE id = %s AND deleted_at IS NOT NULL
		"""
		cur.execute(query, (warehouse_id,))
		return cur.rowcount
	
	@classmethod
	def _get_by_property(
		cls,
		cur: psycopg.Cursor,
		field: Literal["id", "address"],
		value: Any,
		exclude_deleted: bool = True
	) -> Warehouse | None:
		query = f"""
			SELECT {", ".join(cls.SELECT_FIELDS)}
			FROM {cls.TABLE}
			WHERE {field} = %s {'AND deleted_at IS NULL' if exclude_deleted else ''}
			LIMIT 1
		"""
		cur.execute(query, (value,))

		row = cur.fetchone()
		return Warehouse(**row) if row else None
	
	@classmethod
	def get_by_id(
		cls,
		cur: psycopg.Cursor,
		warehouse_id: int,
		exclude_deleted: bool = True
	) -> Warehouse | None:
		return cls._get_by_property(cur, "id", warehouse_id, exclude_deleted)
	
	@classmethod
	def get_by_address(
		cls,
		cur: psycopg.Cursor,
		address: str,
		exclude_deleted: bool = True
	) -> Warehouse | None:
		return cls._get_by_property(cur, "address", address, exclude_deleted)
	
	@classmethod
	def search(
		cls,
		cur: psycopg.Cursor,
		search: str,
		limit: int = 50,
		offset: int = 0,
		exclude_deleted: bool = True
	) -> list[Warehouse]:
		limit, offset = cls.normalize_pagination(limit, offset)
		
		conditions = []
		params = []
		if search:
			conditions.append("address ILIKE %s")
			params.append(f"%{search}%")
		if exclude_deleted:
			conditions.append("deleted_at IS NULL")

		where_clause = cls.build_where(conditions)
		query = f"""
			SELECT {", ".join(cls.SELECT_FIELDS)}
			FROM {cls.TABLE}
			{where_clause}
			ORDER BY created_at DESC
			LIMIT %s
			OFFSET %s
		"""
		params.extend([limit, offset])
		cur.execute(query, tuple(params))
		return [Warehouse(**row) for row in cur.fetchall()]
