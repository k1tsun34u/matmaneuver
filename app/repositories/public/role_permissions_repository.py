import psycopg
from app.models.public.role_permission import RolePermission
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.selectable_mixin import SelectableMixin


class RolePermissionsRepository(
	BaseRepository,
	SelectableMixin[RolePermission]
):
	TABLE = "role_permissions"
	MODEL = RolePermission
	SELECT_FIELDS = (
		"role_id",
		"permission_id",
		"assigned_by",
		"assigned_at",
	)

	ORDER_BY = (("assigned_at", "DESC"),)

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
	def unassign(cls,
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
		cur.execute(query, (permission_ids, role_id, assigned_by,))
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
		cur.execute(query, (permission_ids, role_id,))
		return cur.rowcount
	
	@classmethod
	def get_by_role_id_permission_id(
		cls,
		cur: psycopg.Cursor,
		role_id: int,
		permission_id: int
	) -> RolePermission | None:
		return cls.select(cur, {"role_id": role_id, "permission_id": permission_id})
	
	@classmethod
	def get_many_by_role_id(cls, cur: psycopg.Cursor, role_id: int) -> list[RolePermission]:
		return cls.select_many(cur, {"role_id": role_id})
	
	@classmethod
	def get_many_by_permission_id(cls, cur: psycopg.Cursor, permission_id: int) -> list[RolePermission]:
		return cls.select_many(cur, {"permission_id": permission_id})