import psycopg
from app.utils import Utils
from app.unset import Unset, UNSET
from app.models.public.supplier import Supplier
from app.types.update_result import UpdateResult
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.selectable_mixin import SelectableMixin
from app.repositories.base.mixins.audit_state_mixin import AuditStateMixin


class SuppliersRepository(
	BaseRepository,
	AuditStateMixin,
	SelectableMixin[Supplier]
):
	TABLE = "suppliers"
	MODEL = Supplier
	SELECT_FIELDS = (
		"id",
		"name",
		"phone",
		"email",
		"address",
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
		name: str,
		phone: str,
		email: str | None,
		address: str | None,
		created_by: int | None
	) -> int:
		return cls.execute_create(
			cur=cur,
			table=cls.TABLE,
			fields={
				"name": name,
				"phone": phone,
				"email": email,
				"address": address,
				"created_by": created_by
			},
			returning="id"
		)["id"]
	
	@classmethod
	def update(
		cls,
		cur: psycopg.Cursor,
		supplier_id: int,
		name: str | Unset = UNSET,
		phone: str | Unset = UNSET,
		email: str | None | Unset = UNSET,
		address: str | None | Unset = UNSET
	) -> bool:
		cls.execute_update(
			cur=cur,
			table=cls.TABLE,
			where={"id": supplier_id},
			fields=Utils.filter_unset({
				"name": name,
				"phone": phone,
				"email": email,
				"address": address
			})
		)

		cur.execute(f"SELECT 1 FROM {cls.TABLE} WHERE id = %s", (supplier_id,))
		return bool(cur.fetchone())
	
	@classmethod
	def deactivate(cls, cur: psycopg.Cursor, supplier_id: int, deactivated_by: int) -> UpdateResult:
		return cls.set_state(cur, "deactivated", {"id": supplier_id}, deactivated_by)
	
	@classmethod
	def restore(cls, cur: psycopg.Cursor, supplier_id: int) -> UpdateResult:
		return cls.clear_state(cur, "deactivated", {"id": supplier_id})
	
	@classmethod
	def get_by_id(cls, cur: psycopg.Cursor, supplier_id: int) -> Supplier | None:
		return cls.select(cur, {"id": supplier_id})
	
	@classmethod
	def get_by_phone(cls, cur: psycopg.Cursor, phone: str) -> Supplier | None:
		return cls.select(cur, {"phone": phone})
	
	@classmethod
	def get_by_email(cls, cur: psycopg.Cursor, email: str) -> Supplier | None:
		return cls.select(cur, {"email": email})
	
	@classmethod
	def search(
		cls,
		cur: psycopg.Cursor,
		search: str | None = None,
		limit: int = 50,
		offset: int = 0
	) -> list[Supplier]:
		return cls.select_many(
			cur=cur,
			ilike=(("name", "phone", "email", "address",), f"%{search}%",) if search else None,
			limit=limit,
			offset=offset
		)