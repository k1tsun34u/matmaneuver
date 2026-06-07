import psycopg
from datetime import date
from app.utils import Utils
from typing import ClassVar
from app.models.db.db_user import DbUser
from app.models.public.employee import Employee
from app.types.update_result import UpdateResult
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.selectable_mixin import SelectableMixin
from app.repositories.base.mixins.audit_state_mixin import AuditStateMixin
from app.models.public.employee_user import EmployeeUser


class EmployeesRepository(
	BaseRepository,
	AuditStateMixin,
	SelectableMixin[Employee]
):
	TABLE: ClassVar[str] = Employee.TABLE
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

	ORDER_BY = ((Employee.COLUMN_CREATED_AT, "DESC",),)

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
			table=Employee.TABLE,
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
	def get_by_id(cls, cur: psycopg.Cursor, employee_id: int) -> EmployeeUser | None:
		query = f"""
			SELECT
				e.*,
				u.{DbUser.COLUMN_PHONE},
				u.{DbUser.COLUMN_EMAIL},
				u.{DbUser.COLUMN_FULL_NAME},
				u_firer.{DbUser.COLUMN_FULL_NAME} AS fired_by_{DbUser.COLUMN_FULL_NAME},
				u_hirer.{DbUser.COLUMN_FULL_NAME} AS hired_by_{DbUser.COLUMN_FULL_NAME}
			FROM {Employee.TABLE} AS e
			LEFT JOIN {DbUser.TABLE} AS u ON u.{DbUser.COLUMN_ID} = e.{Employee.COLUMN_USER_ID}
			LEFT JOIN {Employee.TABLE} AS e_firer ON e_firer.{Employee.COLUMN_ID} = e.{Employee.COLUMN_FIRED_BY}
			LEFT JOIN {DbUser.TABLE} AS u_firer ON u_firer.{DbUser.COLUMN_ID} = e_firer.{Employee.COLUMN_USER_ID}
			LEFT JOIN {Employee.TABLE} AS e_hirer ON e_hirer.{Employee.COLUMN_ID} = e.{Employee.COLUMN_HIRED_BY}
			LEFT JOIN {DbUser.TABLE} AS u_hirer ON u_hirer.{DbUser.COLUMN_ID} = e_hirer.{Employee.COLUMN_USER_ID}
			WHERE e.{Employee.COLUMN_ID} = %s
		"""
		cur.execute(query, (employee_id,))
		row = cur.fetchone()
		return EmployeeUser(**row) if row else None
	
	@classmethod
	def get_by_user_id(cls, cur: psycopg.Cursor, user_id: int) -> Employee | None:
		return cls.select(cur=cur, equals={Employee.COLUMN_USER_ID: user_id})
	
	@classmethod
	def search(
		cls,
		cur: psycopg.Cursor,
		search: str | None = None,
		exclude_fired: bool = True,
		limit: int = 50,
		offset: int = 0,
	) -> tuple[list[EmployeeUser], int]:
		conditions, params = Utils.build_conditions_params(
			is_null=(f"e.{Employee.COLUMN_FIRED_AT}",) if exclude_fired else None,
			ilike=(
				(
					f"u.{DbUser.COLUMN_PHONE}",
					f"u.{DbUser.COLUMN_EMAIL}",
					f"u.{DbUser.COLUMN_FULL_NAME}",
				), f"%{search}%",
			) if search else None
		)

		query_part = f"""
			FROM {Employee.TABLE} e
			LEFT JOIN {DbUser.TABLE} AS u ON u.{DbUser.COLUMN_ID} = e.{Employee.COLUMN_USER_ID}
			LEFT JOIN {Employee.TABLE} AS e_firer ON e_firer.{Employee.COLUMN_ID} = e.{Employee.COLUMN_FIRED_BY}
			LEFT JOIN {DbUser.TABLE} AS u_firer ON u_firer.{DbUser.COLUMN_ID} = e_firer.{Employee.COLUMN_USER_ID}
			LEFT JOIN {Employee.TABLE} AS e_hirer ON e_hirer.{Employee.COLUMN_ID} = e.{Employee.COLUMN_HIRED_BY}
			LEFT JOIN {DbUser.TABLE} AS u_hirer ON u_hirer.{DbUser.COLUMN_ID} = e_hirer.{Employee.COLUMN_USER_ID}
			{Utils.build_where(conditions)}
		"""

		query = f"""
			SELECT
				e.*,
				u.{DbUser.COLUMN_PHONE},
				u.{DbUser.COLUMN_EMAIL},
				u.{DbUser.COLUMN_FULL_NAME},
				u_firer.{DbUser.COLUMN_FULL_NAME} AS fired_by_{DbUser.COLUMN_FULL_NAME},
				u_hirer.{DbUser.COLUMN_FULL_NAME} AS hired_by_{DbUser.COLUMN_FULL_NAME}
			{query_part}
			{Utils.build_order_by(cls.ORDER_BY)}
			LIMIT %s
			OFFSET %s
		"""
		cur.execute(query, params + (limit, offset,))
		employee_users = [EmployeeUser(**row) for row in cur.fetchall()]

		query = f"""
			SELECT COUNT(*) AS total
			{query_part}
		"""
		cur.execute(query, params)
		return (employee_users, cur.fetchone()['total'],)

