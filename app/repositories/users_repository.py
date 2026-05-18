import psycopg
from typing import Any, Literal
from datetime import datetime, timezone
from app.unset import Unset, UNSET
from app.models.db.db_user import DbUser
from app.repositories.base_repository import BaseRepository


class UsersRepository(BaseRepository):
	TABLE = "users"
	SELECT_FIELDS = [
		"id",
		"phone",
		"email",
		"full_name",
		"password_hash",
		"blocked_at",
		"deleted_at",
		"created_at"
	]

	@classmethod
	def create(
		cls,
		cur: psycopg.Cursor,
		phone: str,
		email: str | None,
		full_name: str,
		password_hash: str
	) -> int:
		return cls.execute_create(
			cur=cur,
			table=cls.TABLE,
			fields={
				"phone": phone,
				"email": email,
				"full_name": full_name,
				"password_hash": password_hash
			},
			returning="id"
		)["id"]
	
	@classmethod
	def update(
		cls,
		cur: psycopg.Cursor,
		user_id: int,
		phone: str | Unset = UNSET,
		email: str | Unset = UNSET,
		full_name: str | Unset = UNSET,
		password_hash: str | Unset = UNSET,
		blocked_at: datetime | None | Unset = UNSET,
		deleted_at: datetime | None | Unset = UNSET
	) -> int:
		return cls.execute_update(
			cur=cur,
			table=cls.TABLE,
			where={"id": user_id},
			fields=cls.filter_unset({
				"phone": phone,
				"email": email,
				"full_name": full_name,
				"password_hash": password_hash,
				"blocked_at": blocked_at,
				"deleted_at": deleted_at
			})
		)
	
	@classmethod
	def soft_delete(
		cls,
		cur: psycopg.Cursor,
		user_id: int
	) -> int:
		return cls.execute_update(
			cur=cur,
			table=cls.TABLE,
			where={"id": user_id},
			fields={
				"deleted_at": datetime.now(timezone.utc)
			}
		)
	
	@classmethod
	def restore(
		cls,
		cur: psycopg.Cursor,
		user_id: int
	) -> int:
		return cls.execute_update(
			cur=cur,
			table=cls.TABLE,
			where={"id": user_id},
			fields={
				"deleted_at": None
			}
		)
	
	@classmethod
	def block(
		cls,
		cur: psycopg.Cursor,
		user_id: int
	) -> int:
		return cls.execute_update(
			cur=cur,
			table=cls.TABLE,
			where={"id": user_id},
			fields={
				"blocked_at": datetime.now(timezone.utc)
			}
		)
	
	@classmethod
	def unblock(
		cls,
		cur: psycopg.Cursor,
		user_id: int
	) -> int:
		return cls.execute_update(
			cur=cur,
			table=cls.TABLE,
			where={"id": user_id},
			fields={
				"blocked_at": None
			}
		)
	
	@classmethod
	def _get_by_property(
		cls,
		cur: psycopg.Cursor,
		field: Literal["id", "phone", "email"],
		value: Any
	) -> DbUser | None:
		row = cls.execute_select_one(
			cur=cur,
			table=cls.TABLE,
			where={field: value}
		)

		return DbUser(**row) if row else None
	
	@classmethod
	def get_by_id(
		cls,
		cur: psycopg.Cursor,
		user_id: int
	) -> DbUser | None:
		return cls._get_by_property(cur, "id", user_id)
	
	@classmethod
	def get_by_phone(
		cls,
		cur: psycopg.Cursor,
		phone: str
	) -> DbUser | None:
		return cls._get_by_property(cur, "phone", phone)
	
	@classmethod
	def get_by_email(
		cls,
		cur: psycopg.Cursor,
		email: str
	) -> DbUser | None:
		return cls._get_by_property(cur, "email", email)
	
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
		limit, offset = cls.normalize_pagination(limit, offset)

		conditions = []
		params = []
		if exclude_deleted: conditions.append("deleted_at IS NULL")
		if exclude_blocked: conditions.append("blocked_at IS NULL")

		if search:
			condition, search_params = cls.ilike_any(["phone", "email", "full_name"], f"%{search}%")
			conditions.append(condition)
			params.extend(search_params)

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
		return [DbUser(**row) for row in cur.fetchall()]
