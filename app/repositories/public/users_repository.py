
import psycopg
from app.utils import Utils
from app.unset import Unset, UNSET
from app.models.db.db_user import DbUser
from app.types.update_result import UpdateResult
from app.types.token_payload import TokenPayload
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.updatable_mixin import UpdatableMixin
from app.repositories.base.mixins.selectable_mixin import SelectableMixin
from app.repositories.base.mixins.audit_state_mixin import AuditStateMixin


class UsersRepository(
	BaseRepository,
	AuditStateMixin,
	UpdatableMixin,
	SelectableMixin[DbUser]
):
	TABLE = "users"
	MODEL = DbUser
	SELECT_FIELDS = (
		"id",
		"phone",
		"email",
		"full_name",
		"password_hash",
		"token_ver",

		"blocked_by",
		"blocked_at",

		"deleted_by",
		"deleted_at",

		"created_by",
		"created_at",
	)

	ORDER_BY = (("created_at", "DESC"),)

	@classmethod
	def create(
		cls,
		cur: psycopg.Cursor,
		phone: str,
		email: str | None,
		full_name: str,
		password_hash: str,
		created_by: int | None
	) -> int:
		return cls.execute_create(
			cur=cur,
			table=cls.TABLE,
			fields={
				"phone": phone,
				"email": email,
				"full_name": full_name,
				"password_hash": password_hash,
				"created_by": created_by
			},
			returning="id"
		)["id"]
	
	@classmethod
	def update(
		cls,
		cur: psycopg.Cursor,
		user_id: int,
		token_ver: int,
		phone: str | Unset = UNSET,
		email: str | Unset = UNSET,
		full_name: str | Unset = UNSET
	) -> UpdateResult:
		return cls.update_by_conditions(
			cur=cur,
			identity_where={"id": user_id},
			condition_where={"token_ver": token_ver},
			fields=Utils.filter_unset({
				"phone": phone,
				"email": email,
				"full_name": full_name
			})
		)
	
	@classmethod
	def set_password(
		cls,
		cur: psycopg.Cursor,
		user_id: int,
		token_ver: int,
		password_hash: str
	) -> TokenPayload | None:
		query = f"""
			UPDATE {cls.TABLE}
			SET password_hash = %s, token_ver = token_ver + 1
			WHERE id = %s AND token_ver = %s
		"""
		cur.execute(query, (password_hash, user_id, token_ver,))
		if cur.rowcount == 0:
			return None
		return TokenPayload(user_id, token_ver + 1)
	
	@classmethod
	def soft_delete(cls, cur: psycopg.Cursor, user_id: int, deleted_by: int | None) -> UpdateResult:
		return cls.set_state(cur, "deleted", {"id": user_id}, deleted_by)
	
	@classmethod
	def restore(cls, cur: psycopg.Cursor, user_id: int) -> UpdateResult:
		return cls.clear_state(cur, "deleted", {"id": user_id})
	
	@classmethod
	def block(cls, cur: psycopg.Cursor, user_id: int, blocked_by: int) -> UpdateResult:
		return cls.set_state(cur, "blocked", {"id": user_id}, blocked_by)
	
	@classmethod
	def unblock(cls, cur: psycopg.Cursor, user_id: int) -> UpdateResult:
		return cls.clear_state(cur, "blocked", {"id": user_id})
	
	@classmethod
	def get_by_id(cls, cur: psycopg.Cursor, user_id: int) -> DbUser | None:
		return cls.select(cur=cur, equals={"id": user_id})
	
	@classmethod
	def get_by_phone(cls, cur: psycopg.Cursor, phone: str) -> DbUser | None:
		return cls.select(cur=cur, equals={"phone": phone})
	
	@classmethod
	def get_by_email(cls, cur: psycopg.Cursor, email: str) -> DbUser | None:
		return cls.select(cur=cur, equals={"email": email})
	
	@classmethod
	def search(
		cls,
		cur: psycopg.Cursor,
		search: str | None = None,
		exclude_deleted: bool = True,
		exclude_blocked: bool = True,
		limit: int = 50,
		offset: int = 0
	) -> list[DbUser]:
		is_null = tuple()
		if exclude_deleted:
			is_null = is_null + ("deleted_at",)
		if exclude_blocked:
			is_null = is_null + ("blocked_at",)
		return cls.select_many(
			cur=cur,
			is_null=is_null,
			ilike=(("phone", "email", "full_name",), f"%{search}%",) if search else None,
			limit=limit,
			offset=offset
		)