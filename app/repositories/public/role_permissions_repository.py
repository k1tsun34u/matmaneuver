import psycopg
from typing import ClassVar
from collections.abc import Sequence
from app.models.public.role_permission import RolePermission
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.relation_mixin import RelationMixin
from app.repositories.base.mixins.selectable_mixin import SelectableMixin


class RolePermissionsRepository(
	BaseRepository,
	RelationMixin,
	SelectableMixin[RolePermission]
):
	TABLE: ClassVar[str] = RolePermission.TABLE
	MODEL = RolePermission
	TABLE_COLUMNS = (
		RolePermission.COLUMN_ROLE_ID,
		RolePermission.COLUMN_PERMISSION_ID,
		RolePermission.COLUMN_ASSIGNED_BY,
		RolePermission.COLUMN_ASSIGNED_AT,
	)

	ORDER_BY = ((RolePermission.COLUMN_ASSIGNED_AT, "DESC",),)

	@classmethod
	def assign(
		cls,
		cur: psycopg.Cursor,
		role_id: int,
		permission_id: int,
		assigned_by: int | None
	) -> None:
		cls.create_relation(
			cur=cur,
			fixed_field=RolePermission.COLUMN_ROLE_ID,
			fixed_value=role_id,
			varying_field=RolePermission.COLUMN_PERMISSION_ID,
			varying_value=permission_id,
			actor_id=assigned_by
		)
	
	@classmethod
	def unassign(cls,
		cur: psycopg.Cursor,
		role_id: int,
		permission_id: int
	) -> None:
		cls.delete_relation(
			cur=cur,
			fixed_field=RolePermission.COLUMN_ROLE_ID,
			fixed_value=role_id,
			varying_field=RolePermission.COLUMN_PERMISSION_ID,
			varying_value=permission_id
		)
	
	@classmethod
	def assign_many(
		cls,
		cur: psycopg.Cursor,
		role_id: int,
		permission_ids: Sequence[int],
		assigned_by: int | None
	) -> None:
		cls.create_relations(
			cur=cur,
			fixed_field=RolePermission.COLUMN_ROLE_ID,
			fixed_value=role_id,
			varying_field=RolePermission.COLUMN_PERMISSION_ID,
			varying_values=permission_ids,
			actor_id=assigned_by
		)
	
	@classmethod
	def unassign_many(
		cls,
		cur: psycopg.Cursor,
		role_id: int,
		permission_ids: Sequence[int]
	) -> None:
		cls.delete_relations(
			cur=cur,
			fixed_field=RolePermission.COLUMN_ROLE_ID,
			fixed_value=role_id,
			varying_field=RolePermission.COLUMN_PERMISSION_ID,
			varying_values=permission_ids
		)
	
	@classmethod
	def get_by_role_id_permission_id(
		cls,
		cur: psycopg.Cursor,
		role_id: int,
		permission_id: int
	) -> RolePermission | None:
		return cls.select(
			cur, {
				RolePermission.COLUMN_ROLE_ID: role_id,
				RolePermission.COLUMN_PERMISSION_ID: permission_id
			}
		)
	
	@classmethod
	def get_many_by_role_id(cls, cur: psycopg.Cursor, role_id: int) -> list[RolePermission]:
		return cls.select_many(cur, {RolePermission.COLUMN_ROLE_ID: role_id})
	
	@classmethod
	def get_many_by_permission_id(cls, cur: psycopg.Cursor, permission_id: int) -> list[RolePermission]:
		return cls.select_many(cur, {RolePermission.COLUMN_PERMISSION_ID: permission_id})
