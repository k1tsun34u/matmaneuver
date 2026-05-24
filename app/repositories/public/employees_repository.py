import psycopg
from datetime import date
from app.models.public.employee import Employee
from app.types.update_result import UpdateResult
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
	TABLE_COLUMNS = (
		Employee.COLUMN_ID,
		Employee.COLUMN_USER_ID,
		Employee.COLUMN_HIRED_BY,
		Employee.COLUMN_HIRED_AT,
		Employee.COLUMN_FIRED_BY,
		Employee.COLUMN_FIRED_AT,
		Employee.COLUMN_CREATED_BY,
		Employee.COLUMN_CREATED_AT,
	)

	ORDER_BY = ((Employee.COLUMN_CREATED_AT, "DESC"),)

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
				Employee.COLUMN_USER_ID: user_id,
				Employee.COLUMN_HIRED_BY: hired_by,
				Employee.COLUMN_HIRED_AT: hired_at,
				Employee.COLUMN_CREATED_BY: created_by
			},
			returning=Employee.COLUMN_ID
		)[Employee.COLUMN_ID]
	
	@classmethod
	def fire(cls, cur: psycopg.Cursor, employee_id: int, fired_by: int) -> UpdateResult:
		return cls.set_state(cur, "fired", {Employee.COLUMN_ID: employee_id}, fired_by)
	
	@classmethod
	def rehire(cls, cur: psycopg.Cursor, employee_id: int, hired_by: int | None) -> UpdateResult:
		tmp = cls.clear_state(cur, "fired", {Employee.COLUMN_ID: employee_id})
		if tmp != UpdateResult.SUCCESS:
			return tmp
		if hired_by:
			return cls.set_state(cur, "hired", {Employee.COLUMN_ID: employee_id})
		return tmp
		
	@classmethod
	def get_by_id(cls, cur: psycopg.Cursor, employee_id: int) -> Employee | None:
		return cls.select(cur=cur, equals={Employee.COLUMN_ID: employee_id})
	
	@classmethod
	def get_by_user_id(cls, cur: psycopg.Cursor, user_id: int) -> Employee | None:
		return cls.select(cur=cur, equals={Employee.COLUMN_USER_ID: user_id})
	
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
			is_null=(Employee.COLUMN_FIRED_AT,) if exclude_fired else None,
			limit=limit,
			offset=offset
		)
