import psycopg
from app.utils import Utils
from typing import Any, Literal, ClassVar, Generic, TypeVar


T = TypeVar("T")

class SelectableMixin(Generic[T]):
	"""
		Implements:
		+ select(...)
		+ select_many(...)

		Requires class vars:
		- TABLE
		- MODEL
		- TABLE_COLUMNS
		- ORDER_BY
	"""

	MODEL: ClassVar[type[T]]
	TABLE_COLUMNS: ClassVar[tuple[str, ...]]
	ORDER_BY: ClassVar[tuple[tuple[str, Literal["ASC", "DESC"]], ...]]

	@classmethod
	def select(
		cls,
		cur: psycopg.Cursor,
		equals: dict[str, Any] | None = None,
		is_null: tuple[str, ...] | None = None,
		is_not_null: tuple[str, ...] | None = None,
		ilike: tuple[tuple[str, ...], str] | None = None
	) -> T | None:
		conditions, params = Utils.build_conditions_params(
			equals=equals,
			is_null=is_null,
			is_not_null=is_not_null,
			ilike=ilike
		)

		query = Utils.build_select_statement(
			select_fields=cls.TABLE_COLUMNS,
			table=cls.TABLE,
			conditions=conditions,
			order_by=cls.ORDER_BY,
			many=False
		)

		cur.execute(query, params)
		row = cur.fetchone()
		return cls.MODEL(**row) if row else None
	
	@classmethod
	def select_many(
		cls,
		cur: psycopg.Cursor,
		equals: dict[str, Any] | None = None,
		is_null: tuple[str, ...] | None = None,
		is_not_null: tuple[str, ...] | None = None,
		ilike: tuple[tuple[str, ...], str] | None = None,
		limit: int = 50,
		offset: int = 0
	) -> list[T]:
		limit, offset = Utils.normalize_pagination(limit, offset)
		conditions, params = Utils.build_conditions_params(
			equals=equals,
			is_null=is_null,
			is_not_null=is_not_null,
			ilike=ilike
		)

		query = Utils.build_select_statement(
			select_fields=cls.TABLE_COLUMNS,
			table=cls.TABLE,
			conditions=conditions,
			order_by=cls.ORDER_BY,
			many=True
		)

		cur.execute(query, (*params, limit, offset,))
		rows = cur.fetchall()
		return [cls.MODEL(**row) for row in rows]