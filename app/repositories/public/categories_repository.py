import psycopg
from typing import ClassVar
from app.models.public.category import Category
from app.types.update_result import UpdateResult
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.updatable_mixin import UpdatableMixin
from app.repositories.base.mixins.selectable_mixin import SelectableMixin
from app.repositories.base.mixins.audit_state_mixin import AuditStateMixin
from app.utils import Utils


class CategoriesRepository(
	BaseRepository,
	AuditStateMixin,
	UpdatableMixin,
	SelectableMixin[Category]
):
	TABLE: ClassVar[str] = Category.TABLE
	MODEL = Category
	TABLE_COLUMNS = (
		Category.COLUMN_ID,
		Category.COLUMN_PARENT_CATEGORY_ID,
		Category.COLUMN_NAME,
		Category.COLUMN_DEACTIVATED_BY,
		Category.COLUMN_DEACTIVATED_AT,
		Category.COLUMN_CREATED_BY,
		Category.COLUMN_CREATED_AT,
	)

	ORDER_BY = ((Category.COLUMN_CREATED_AT, "DESC",),)

	@classmethod
	def create(
		cls,
		cur: psycopg.Cursor,
		parent_category_id: int | None,
		name: str,
		created_by: int | None
	) -> int:
		return cls.execute_create(
			cur=cur,
			table=cls.TABLE,
			fields={
				Category.COLUMN_PARENT_CATEGORY_ID: parent_category_id,
				Category.COLUMN_NAME: name,
				Category.COLUMN_CREATED_BY: created_by
			},
			returning=Category.COLUMN_ID
		)[Category.COLUMN_ID]
	
	@classmethod
	def set_parent_category(
		cls,
		cur: psycopg.Cursor,
		category_id: int,
		parent_category_id: int | None
	) -> UpdateResult:
		return cls.update_by_conditions(
			cur=cur,
			identity_where={Category.COLUMN_ID: category_id},
			fields={Category.COLUMN_PARENT_CATEGORY_ID: parent_category_id}
		)
	
	@classmethod
	def deactivate(cls, cur: psycopg.Cursor, category_id: int, deactivated_by: int) -> UpdateResult:
		return cls.set_state(cur, "deactivated", {Category.COLUMN_ID: category_id}, deactivated_by)
	
	@classmethod
	def restore(cls, cur: psycopg.Cursor, category_id: int) -> UpdateResult:
		return cls.clear_state(cur, "deactivated", {Category.COLUMN_ID: category_id})
	
	@classmethod
	def get_by_id(cls, cur: psycopg.Cursor, category_id: int) -> Category | None:
		return cls.select(cur, {Category.COLUMN_ID: category_id})
	
	@classmethod
	def get_by_name(cls, cur: psycopg.Cursor, name: str) -> Category | None:
		return cls.select(cur, {Category.COLUMN_NAME: name})
	
	@classmethod
	def search(
		cls,
		cur: psycopg.Cursor,
		search: str | None = None,
		exclude_deactivated: bool = True,
		limit: int = 50,
		offset: int = 0
	) -> tuple[list[Category], int]:
		is_null=(Category.COLUMN_DEACTIVATED_AT,) if exclude_deactivated else None
		ilike=((Category.COLUMN_NAME,), f"%{search}%",) if search else None
		categories = cls.select_many(
			cur=cur,
			is_null=is_null,
			ilike=ilike,
			limit=limit,
			offset=offset
		)

		conditions, params = Utils.build_conditions_params(
			is_null=is_null,
			ilike=ilike
		)

		query = f"""
			SELECT COUNT(*) AS total
			FROM {cls.TABLE}
			{Utils.build_where(conditions)}
		"""
		cur.execute(query, params)
		return (categories, cur.fetchone()['total'],)
