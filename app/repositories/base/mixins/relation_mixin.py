import psycopg
from typing import ClassVar
from collections.abc import Sequence


class RelationMixin:
	"""
		Only for M:N link tables. Table should have following form:
		- <prim_key_first_part>: int
		- <prim_key_second_part>: int
		- assigned_by: int | None
		- assigned_at: datetime

		Implements:
		+ create_relation(...)
		+ delete_relation(...)
		+ create_relations(...)
		+ delete_relations(...)

		Requires class vars:
		- TABLE
		- TABLE_COLUMNS
	"""
	
	TABLE_COLUMNS: ClassVar[tuple[str, ...]]

	@classmethod
	def create_relation(
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

		cls.create_relations(
			cur=cur,
			fixed_field=fixed_field,
			fixed_value=fixed_value,
			varying_field=varying_field,
			varying_values=(varying_value,),
			actor_id=actor_id
		)

	@classmethod
	def delete_relation(
		cls,
		cur: psycopg.Cursor,
		fixed_field: str,
		fixed_value: int,
		varying_field: str,
		varying_value: int
	) -> None:
		"""
			May cause:
			- UnhandledError
		"""

		cls.delete_relations(
			cur=cur,
			fixed_field=fixed_field,
			fixed_value=fixed_value,
			varying_field=varying_field,
			varying_values=(varying_value,)
		)
	
	@classmethod
	def create_relations(
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
	def delete_relations(
		cls,
		cur: psycopg.Cursor,
		fixed_field: str,
		fixed_value: int,
		varying_field: str,
		varying_values: Sequence[int]
	) -> None:
		"""
			May cause:
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
