import psycopg
from datetime import date
from app.models.public.employee import Employee
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.selectable_mixin import SelectableMixin
from app.repositories.base.mixins.audit_state_mixin import AuditStateMixin


class EmployeesRepository(
	BaseRepository,
	AuditStateMixin,
	SelectableMixin[Employee]
):
	TABLE = "employees"
	MODEL = Employee
	SELECT_FIELDS = (
		"id",
		"user_id",
		"hired_by",
		"hired_at",
		"fired_by",
		"fired_at",
		"created_by",
		"created_at",
	)

	ORDER_BY = (("created_at", "DESC"),)

	@classmethod
	def create(
		cls,
		cur: psycopg.Cursor,
		user_id: int,
		hired_by: int | None,
		hired_at: date,
		created_by: int | None
	) -> int:
		return cls.execute_create(
			cur=cur,
			table=cls.TABLE,
			fields={
				"user_id": user_id,
				"hired_by": hired_by,
				"hired_at": hired_at,
				"created_by": created_by
			},
			returning="id"
		)["id"]
	
	@classmethod
	def fire(cls, cur: psycopg.Cursor, employee_id: int, fired_by: int) -> int:
		return cls.set_state(cur, "fired", {"id": employee_id}, fired_by)
	
	@classmethod
	def rehire(cls, cur: psycopg.Cursor, employee_id: int) -> int:
		return cls.clear_state(cur, "fired", {"id": employee_id})
	
	@classmethod
	def get_by_id(cls, cur: psycopg.Cursor, employee_id: int) -> Employee | None:
		return cls.select(cur=cur, equals={"id": employee_id})
	
	@classmethod
	def get_by_user_id(cls, cur: psycopg.Cursor, user_id: int) -> Employee | None:
		return cls.select(cur=cur, equals={"user_id": user_id})
	
	@classmethod
	def get_many(
		cls,
		cur: psycopg.Cursor,
		exclude_fired: bool = True,
		limit: int = 50,
		offset: int = 0,
	) -> list[Employee]:
		return cls.select_many(
			cur=cur,
			is_null=("fired_at",) if exclude_fired else None,
			limit=limit,
			offset=offset
		)