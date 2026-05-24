import psycopg
from typing import ClassVar
from collections.abc import Sequence


class AssignableMixin:
	"""
		Only for M:N link tables. Table should have following form:
		- <prim_key_first_part>: int
		- <prim_key_second_part>: int
		- assigned_by: int | None
		- assigned_at: datetime

		Implements:
		+ assign_by_conditions(...)
		+ unassign_by_conditions(...)
		+ assign_many_by_conditions(...)
		+ unassign_many_by_conditions(...)

		Requires class vars:
		- TABLE
		- TABLE_COLUMNS

		Requires methods:
		- execute_update(...)
		- execute_delete(...)
	"""
	
	TABLE_COLUMNS: ClassVar[tuple[str, ...]]

	@classmethod
	def assign_by_fields(
		cls,
		cur: psycopg.Cursor,
		fixed_field: str,
		fixed_value: int,
		varying_field: str,
		varying_value: int,
		actor_id: int | None
	) -> None:
		"""
			May cause:
			- NotFoundError
			- UnhandledError
		"""

		cls.assign_many_by_fields(
			cur=cur,
			fixed_field=fixed_field,
			fixed_value=fixed_value,
			varying_field=varying_field,
			varying_values=(varying_value,),
			actor_id=actor_id
		)

	@classmethod
	def unassign_by_fields(
		cls,
		cur: psycopg.Cursor,
		fixed_field: str,
		fixed_value: int,
		varying_field: str,
		varying_value: int
	) -> None:
		"""
			May cause:
			- NotFoundError
			- UnhandledError
		"""

		cls.unassign_many_by_fields(
			cur=cur,
			fixed_field=fixed_field,
			fixed_value=fixed_value,
			varying_field=varying_field,
			varying_values=(varying_value,)
		)
	
	@classmethod
	def assign_many_by_fields(
		cls,
		cur: psycopg.Cursor,
		fixed_field: str,
		fixed_value: int,
		varying_field: str,
		varying_values: Sequence[int],
		actor_id: int | None
	) -> None:
		"""
			May cause:
			- NotFoundError
			- UnhandledError
		"""

		varying_values = list(dict.fromkeys(varying_values))
		if not varying_values:
			return
		
		query = f"""
			INSERT INTO {cls.TABLE} ({", ".join(cls.TABLE_COLUMNS)})
			SELECT
				%s,
				unnest(%s::bigint[]),
				%s,
				NOW()
			ON CONFLICT ({fixed_field}, {varying_field}) DO NOTHING
		"""
		cur.execute(query, (fixed_value, varying_values, actor_id,))
	
	@classmethod
	def unassign_many_by_fields(
		cls,
		cur: psycopg.Cursor,
		fixed_field: str,
		fixed_value: int,
		varying_field: str,
		varying_values: Sequence[int]
	) -> None:
		"""
			May cause:
			- NotFoundError
			- UnhandledError
		"""

		varying_values = list(dict.fromkeys(varying_values))
		if not varying_values:
			return
		
		query = f"""
			DELETE FROM {cls.TABLE} target
			USING (
				SELECT unnest(%s::bigint[]) AS {varying_field}
			) source
			WHERE
				target.{fixed_field} = %s
				AND target.{varying_field} = source.{varying_field}
		"""
		cur.execute(query, (varying_values, fixed_value,))
