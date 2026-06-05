import psycopg
from app.models.public.role import Role
from app.models.public.employee import Employee
from app.models.public.permission import Permission
from app.models.public.employee_role import EmployeeRole
from app.models.public.role_permission import RolePermission
from app.repositories.base.base_repository import BaseRepository


class EmployeePermissionsRepository(BaseRepository):
	@classmethod
	def get_permissions(cls, cur: psycopg.Cursor, employee_id: int) -> list[Permission]:
		query = f"""
			SELECT DISTINCT p.*
			FROM permissions p
			JOIN role_permissions rp ON rp.{RolePermission.COLUMN_PERMISSION_ID} = p.{Permission.COLUMN_ID}
			JOIN employee_roles er ON er.{EmployeeRole.COLUMN_ROLE_ID} = rp.{RolePermission.COLUMN_ROLE_ID}
			JOIN roles r ON r.{Role.COLUMN_ID} = rp.{RolePermission.COLUMN_ROLE_ID}
			JOIN employees e ON e.{Employee.COLUMN_ID} = er.{EmployeeRole.COLUMN_EMPLOYEE_ID}
			WHERE
				er.{EmployeeRole.COLUMN_EMPLOYEE_ID} = %s
				AND r.{Role.COLUMN_DEACTIVATED_AT} IS NULL
				AND p.{Permission.COLUMN_DEACTIVATED_AT} IS NULL
				AND e.{Employee.COLUMN_FIRED_AT} IS NULL
		"""
		cur.execute(query, (employee_id,))
		return [Permission(**row) for row in cur.fetchall()]
	
	@classmethod
	def has_permission(cls, cur: psycopg.Cursor, employee_id: int, code: str) -> bool:
		query = f"""
			SELECT EXISTS(
				SELECT 1
				FROM employee_roles er
				JOIN role_permissions rp ON rp.{RolePermission.COLUMN_ROLE_ID} = er.{EmployeeRole.COLUMN_ROLE_ID}
				JOIN roles r ON r.{Role.COLUMN_ID} = rp.{RolePermission.COLUMN_ROLE_ID}
				JOIN permissions p ON p.{Permission.COLUMN_ID} = rp.{RolePermission.COLUMN_PERMISSION_ID}
				JOIN employees e ON e.{Employee.COLUMN_ID} = er.{EmployeeRole.COLUMN_EMPLOYEE_ID}
				WHERE
					er.{EmployeeRole.COLUMN_EMPLOYEE_ID} = %s
					AND r.{Role.COLUMN_DEACTIVATED_AT} IS NULL
					AND p.{Permission.COLUMN_CODE} = %s
					AND p.{Permission.COLUMN_DEACTIVATED_AT} IS NULL
					AND e.{Employee.COLUMN_FIRED_AT} IS NULL
			)
		"""
		cur.execute(query, (employee_id, code,))
		return bool(cur.fetchone()['exists'])
