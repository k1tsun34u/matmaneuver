import psycopg
from app.models.public.permission import Permission
from app.repositories.base.base_repository import BaseRepository


class EmployeePermissionsRepository(BaseRepository):
	TABLE = ""
	
	@classmethod
	def get_permissions(cls, cur: psycopg.Cursor, employee_id: int) -> list[Permission]:
		query = """
			SELECT DISTINCT p.*
			FROM permissions p
			JOIN role_permissions rp ON rp.permission_id = p.id
			JOIN employee_roles er ON er.role_id = rp.role_id
			WHERE er.employee_id = %s AND p.deactivated_at IS NULL
		"""
		cur.execute(query, (employee_id,))
		return [Permission(**row) for row in cur.fetchall()]
	
	@classmethod
	def has_permission(cls, cur: psycopg.Cursor, employee_id: int, code: str) -> bool:
		query = """
			SELECT EXISTS(
				SELECT 1
				FROM employee_roles er
				JOIN role_permissions rp ON rp.role_id = er.role_id
				JOIN permissions p ON p.id = rp.permission_id
				WHERE
					er.employee_id = %s
					AND p.code = %s
					AND p.deactivated_at IS NULL
			)
		"""
		cur.execute(query, (employee_id, code,))
		return bool(cur.fetchone()[0])
