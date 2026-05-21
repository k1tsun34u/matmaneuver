import psycopg
from app.models.public.category import Category
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.selectable_mixin import SelectableMixin
from app.repositories.base.mixins.audit_state_mixin import AuditStateMixin


class CategoriesRepository(
	BaseRepository,
	AuditStateMixin,
	SelectableMixin[Category]
):
	TABLE = "categories"
	MODEL = Category
	SELECT_FIELDS = (
		"id",
		"parent_category_id",
		"name",
		"deactivated_by",
		"deactivated_at",
		"created_by",
		"created_at",
	)

	ORDER_BY = (("created_at", "DESC"),)

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
				"parent_category_id": parent_category_id,
				"name": name,
				"created_by": created_by
			},
			returning="id"
		)["id"]
	
	@classmethod
	def set_parent_category(
		cls,
		cur: psycopg.Cursor,
		category_id: int,
		parent_category_id: int | None
	) -> bool:
		cls.execute_update(
			cur=cur,
			table=cls.TABLE,
			where={"id": category_id},
			fields={"parent_category_id": parent_category_id}
		)

		cur.execute(f"SELECT 1 FROM {cls.TABLE} WHERE id = %s", (category_id,))
		return bool(cur.fetchone())
	
	@classmethod
	def deactivate(cls, cur: psycopg.Cursor, category_id: int, deactivated_by: int) -> int:
		return cls.set_state(cur, "deactivated", {"id": category_id}, deactivated_by)
	
	@classmethod
	def restore(cls, cur: psycopg.Cursor, category_id: int) -> int:
		return cls.clear_state(cur, "deactivated", {"id": category_id})
	
	@classmethod
	def get_by_id(cls, cur: psycopg.Cursor, category_id: int) -> Category | None:
		return cls.select(cur, {"id": category_id})
	
	@classmethod
	def get_by_name(cls, cur: psycopg.Cursor, name: str) -> Category | None:
		return cls.select(cur, {"name": name})
	
	@classmethod
	def search(
		cls,
		cur: psycopg.Cursor,
		search: str | None = None,
		exclude_deactivated: bool = True,
		limit: int = 50,
		offset: int = 0
	) -> list[Category]:
		return cls.select_many(
			cur=cur,
			is_null=("deactivated_at",) if exclude_deactivated else None,
			ilike=(("name",), f"%{search}%",) if search else None,
			limit=limit,
			offset=offset
		)