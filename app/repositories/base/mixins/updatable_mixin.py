import psycopg
from typing import Any
from app.utils import Utils
from app.types.update_result import UpdateResult


class UpdatableMixin:
	"""
		Implements:
		+ update(...)

		Requires class vars:
		- TABLE

		Requires methods:
		- execute_update(...)
	"""

	@classmethod
	def update_by_conditions(
		cls,
		cur: psycopg.Cursor,
		identity_where: dict[str, Any],
		condition_where: dict[str, Any],
		fields: dict[str, Any]
	) -> UpdateResult:
		count = cls.execute_update(
			cur=cur,
			table=cls.TABLE,
			where=identity_where | condition_where,
			fields=fields
		)

		if count != 0:
			return UpdateResult.SUCCESS

		prim_conditions, prim_params = Utils.build_conditions_params(equals=identity_where)
		query = f"""
			SELECT 1 FROM {cls.TABLE}
			{Utils.build_where(prim_conditions)}
		"""
		cur.execute(query, prim_params)
		if not cur.fetchone():
			return UpdateResult.FAIL_NOT_FOUND
		return UpdateResult.FAIL_CONDITION
