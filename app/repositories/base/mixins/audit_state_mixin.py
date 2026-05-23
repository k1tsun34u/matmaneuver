import psycopg
from typing import Any
from app.utils import Utils
from app.types.update_result import UpdateResult


class AuditStateMixin:
	"""
		Implements:
		+ set_state(...)
		+ clear_state(...)

		Requires class vars:
		- TABLE
	"""

	@classmethod
	def set_state(
		cls,
		cur: psycopg.Cursor,
		state: str,
		properties: dict[str, Any],
		actor_id: int | None
	) -> UpdateResult:
		conditions, params = Utils.build_conditions_params(
			equals=properties,
			is_null=(f"{state}_at",)
		)

		query = f"""
			UPDATE {cls.TABLE}
			SET
				{state}_by = %s,
				{state}_at = NOW()
			{Utils.build_where(conditions)}
		"""
		cur.execute(query, (actor_id, *params,))
		if cur.rowcount != 0:
			return UpdateResult.SUCCESS
		
		conditions, params = Utils.build_conditions_params(equals=properties)
		query = f"""
			SELECT 1 FROM {cls.TABLE}
			{Utils.build_where(conditions)}
		"""
		cur.execute(query, params)
		if not cur.fetchone():
			return UpdateResult.FAIL_NOT_FOUND
		return UpdateResult.FAIL_CONDITION

	@classmethod
	def clear_state(
		cls,
		cur: psycopg.Cursor,
		state: str,
		properties: dict[str, Any]
	) -> UpdateResult:
		conditions, params = Utils.build_conditions_params(
			equals=properties,
			is_not_null=(f"{state}_at",)
		)

		query = f"""
			UPDATE {cls.TABLE}
			SET
				{state}_by = NULL,
				{state}_at = NULL
			{Utils.build_where(conditions)}
		"""
		cur.execute(query, params)
		if cur.rowcount != 0:
			return UpdateResult.SUCCESS
		
		conditions, params = Utils.build_conditions_params(equals=properties)
		query = f"""
			SELECT 1 FROM {cls.TABLE}
			{Utils.build_where(conditions)}
		"""
		cur.execute(query, params)
		if not cur.fetchone():
			return UpdateResult.FAIL_NOT_FOUND
		return UpdateResult.FAIL_CONDITION
