import psycopg
from typing import Any, Literal
from app.models.public.role_permission import RolePermission
from app.repositories.base_repository import BaseRepository


class RolePermissionsRepository(BaseRepository):
	TABLE = "role_permissions"
	SELECT_FIELDS = [
		"role_id",
		"permission_id",
		"assigned_by",
		"assigned_at"
	]

	@classmethod
	def assign(
		cls,
		cur: psycopg.Cursor,
		role_id: int,
		permission_id: int,
		assigned_by: int | None
	) -> None:
		cls.execute_create(
			cur=cur,
			table=cls.TABLE,
			fields={
				"role_id": role_id,
				"permission_id": permission_id,
				"assigned_by": assigned_by
			},
			returning=None
		)
	
	@classmethod
	def unassign(
		cls,
		cur: psycopg.Cursor,
		role_id: int,
		permission_id: int
	) -> int:
		return cls.execute_delete(cur, cls.TABLE, {
			"role_id": role_id,
			"permission_id": permission_id
		})
	
	@classmethod
	def assign_many(
		cls,
		cur: psycopg.Cursor,
		role_id: int,
		permission_ids: list[int],
		assigned_by: int | None
	) -> int:
		query = f"""
			INSERT INTO {cls.TABLE} ({", ".join(cls.SELECT_FIELDS)})
			SELECT
				%s,
				unnest(%s::bigint[]),
				%s,
				NOW()
			ON CONFLICT (role_id, permission_id) DO NOTHING
		"""
		cur.execute(query, (role_id, permission_ids, assigned_by,))
		return cur.rowcount
	
	@classmethod
	def unassign_many(
		cls,
		cur: psycopg.Cursor,
		role_id: int,
		permission_ids: list[int]
	) -> int:
		query = f"""
			DELETE FROM {cls.TABLE} rp
			USING (
				SELECT unnest(%s::bigint[]) AS permission_id
			) p
			WHERE rp.role_id = %s AND rp.permission_id = p.permission_id
		"""
		cur.execute(query, (role_id, permission_ids,))
		return cur.rowcount
	
	@classmethod
	def get_by_role_id_permission_id(
		cls,
		cur: psycopg.Cursor,
		role_id: int,
		permission_id: int
	) -> RolePermission | None:
		row = cls.execute_select_one(
			cur=cur,
			table=cls.TABLE,
			where={"role_id": role_id, "permission_id": permission_id}
		)

		return RolePermission(**row) if row else None
	
	@classmethod
	def _get_many_by_property(
		cls,
		cur: psycopg.Cursor,
		field: Literal["role_id", "permission_id"],
		value: Any
	) -> list[RolePermission]:
		rows = cls.execute_select(
			cur=cur,
			table=cls.TABLE,
			where={field: value}
		)

		return [RolePermission(**row) for row in rows]
	
	@classmethod
	def get_many_by_role_id(
		cls,
		cur: psycopg.Cursor,
		role_id: int
	) -> list[RolePermission]:
		return cls._get_many_by_property(cur, "role_id", role_id)
	
	@classmethod
	def get_many_by_permission_id(
		cls,
		cur: psycopg.Cursor,
		permission_id: int
	) -> list[RolePermission]:
		return cls._get_many_by_property(cur, "permission_id", permission_id)