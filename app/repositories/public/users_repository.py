
import psycopg
from app.utils import Utils
from typing import ClassVar
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
	TABLE = DbUser.TABLE
	MODEL = DbUser
	TABLE_COLUMNS = (
		DbUser.COLUMN_ID,
		DbUser.COLUMN_PHONE,
		DbUser.COLUMN_EMAIL,
		DbUser.COLUMN_FULL_NAME,
		DbUser.COLUMN_PASSWORD_HASH,
		DbUser.COLUMN_TOKEN_VER,
		DbUser.COLUMN_BLOCKED_BY,
		DbUser.COLUMN_BLOCKED_AT,
		DbUser.COLUMN_DELETED_BY,
		DbUser.COLUMN_DELETED_AT,
		DbUser.COLUMN_CREATED_BY,
		DbUser.COLUMN_CREATED_AT,
	)

	ORDER_BY = ((DbUser.COLUMN_CREATED_AT, "DESC",),)

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
			table=DbUser.TABLE,
			fields={
				DbUser.COLUMN_PHONE: phone,
				DbUser.COLUMN_EMAIL: email,
				DbUser.COLUMN_FULL_NAME: full_name,
				DbUser.COLUMN_PASSWORD_HASH: password_hash,
				DbUser.COLUMN_CREATED_BY: created_by
			},
			returning=DbUser.COLUMN_ID
		)[DbUser.COLUMN_ID]
	
	@classmethod
	def update(
		cls,
		cur: psycopg.Cursor,
		user_id: int,
		token_ver: int,
		norm_phone: str | Unset = UNSET,
		norm_email: str | Unset = UNSET,
		norm_full_name: str | Unset = UNSET
	) -> UpdateResult:
		return cls.update_by_conditions(
			cur=cur,
			identity_where={DbUser.COLUMN_ID: user_id},
			condition_where={DbUser.COLUMN_TOKEN_VER: token_ver},
			fields=Utils.filter_unset({
				DbUser.COLUMN_PHONE: norm_phone,
				DbUser.COLUMN_EMAIL: norm_email,
				DbUser.COLUMN_FULL_NAME: norm_full_name
			})
		)
	
	@classmethod
	def set_password(
		cls,
		cur: psycopg.Cursor,
		user_id: int,
		token_ver: int,
		password_hash: str
	) -> tuple[UpdateResult, TokenPayload | None]:
		next_token_ver = token_ver + 1
		tmp = cls.update_by_conditions(
			cur=cur,
			identity_where={DbUser.COLUMN_ID: user_id},
			condition_where={DbUser.COLUMN_TOKEN_VER: token_ver},
			fields={
				DbUser.COLUMN_PASSWORD_HASH: password_hash,
				DbUser.COLUMN_TOKEN_VER: next_token_ver
			}
		)

		if tmp == UpdateResult.SUCCESS:
			return (tmp, TokenPayload(user_id, next_token_ver),)
		return (tmp, None,)
	
	@classmethod
	def soft_delete(cls, cur: psycopg.Cursor, user_id: int, deleted_by: int | None) -> UpdateResult:
		return cls.set_state(cur, "deleted", {DbUser.COLUMN_ID: user_id}, deleted_by)
	
	@classmethod
	def restore(cls, cur: psycopg.Cursor, user_id: int) -> UpdateResult:
		return cls.clear_state(cur, "deleted", {DbUser.COLUMN_ID: user_id})
	
	@classmethod
	def block(cls, cur: psycopg.Cursor, user_id: int, blocked_by: int) -> UpdateResult:
		return cls.set_state(cur, "blocked", {DbUser.COLUMN_ID: user_id}, blocked_by)
	
	@classmethod
	def unblock(cls, cur: psycopg.Cursor, user_id: int) -> UpdateResult:
		return cls.clear_state(cur, "blocked", {DbUser.COLUMN_ID: user_id})
	
	@classmethod
	def get_by_id(cls, cur: psycopg.Cursor, user_id: int) -> DbUser | None:
		return cls.select(cur=cur, equals={DbUser.COLUMN_ID: user_id})
	
	@classmethod
	def get_by_phone(cls, cur: psycopg.Cursor, phone: str) -> DbUser | None:
		return cls.select(cur=cur, equals={DbUser.COLUMN_PHONE: phone})
	
	@classmethod
	def get_by_email(cls, cur: psycopg.Cursor, email: str) -> DbUser | None:
		return cls.select(cur=cur, equals={DbUser.COLUMN_EMAIL: email})
	
	@classmethod
	def search(
		cls,
		cur: psycopg.Cursor,
		search: str | None = None,
		exclude_deleted: bool = True,
		exclude_blocked: bool = True,
		limit: int = 50,
		offset: int = 0
	) -> tuple[list[DbUser], int]:
		is_null = tuple()
		if exclude_deleted:
			is_null = is_null + (DbUser.COLUMN_DELETED_AT,)
		if exclude_blocked:
			is_null = is_null + (DbUser.COLUMN_BLOCKED_AT,)
		ilike = ((DbUser.COLUMN_PHONE, DbUser.COLUMN_EMAIL, DbUser.COLUMN_FULL_NAME,), f"%{search}%",) if search else None
		users = cls.select_many(
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
		return (users, cur.fetchone()['total'],)
