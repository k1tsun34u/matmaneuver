from typing import Any, Literal
from app.unset import Unset

class Utils:
	@staticmethod
	def normalize_pagination(limit: int, offset: int) -> tuple[int, int]:
		limit = max(1, min(limit, 100))
		offset = max(0, offset)
		return limit, offset

	@staticmethod
	def filter_unset(fields: dict[str, object]) -> dict[str, object]:
		return {k: v for k, v in fields.items() if not isinstance(v, Unset)}

	@staticmethod
	def build_conditions_params(
		equals: dict[str, Any] | None = None,
		is_null: tuple[str, ...] | None = None,
		is_not_null: tuple[str, ...] | None = None,
		ilike: tuple[tuple[str, ...], str] | None = None
	) -> tuple[tuple[str, ...], tuple[Any, ...]]:
		res_conditions = []
		res_params = []
		if equals:
			for k, v in equals.items():
				res_conditions.append(f"{k} = %s")
				res_params.append(v)
		if is_null:
			for name in is_null:
				res_conditions.append(f"{name} IS NULL")
		if is_not_null:
			for name in is_not_null:
				res_conditions.append(f"{name} IS NOT NULL")
		if ilike:
			fields, value = ilike
			ilike_conditions = [f"{field} ILIKE %s" for field in fields]
			res_conditions.append("(" + " OR ".join(ilike_conditions) + ")")
			res_params.extend([value] * len(fields))
		return (tuple(res_conditions), tuple(res_params),)

	@staticmethod
	def build_where(conditions: tuple[str, ...]) -> str:
		return "WHERE " + " AND ".join(conditions) if conditions else ""

	@staticmethod
	def build_order_by(elems: tuple[tuple[str, Literal["ASC", "DESC"]], ...]) -> str:
		res = [f"{field} {direction}" for field, direction in elems]
		return ("ORDER BY " + ", ".join(res)) if res else ""
	
	@classmethod
	def build_select_statement(
		cls,
		select_fields: tuple[str, ...],
		table: str,
		conditions: tuple[str, ...],
		order_by: tuple[tuple[str, Literal["ASC", "DESC"]], ...],
		many: bool = False
	) -> str:
		query = f"""
			SELECT {", ".join(select_fields)}
			FROM {table}
			{cls.build_where(conditions)}
		"""
		if many:
			query += f"""
				{cls.build_order_by(order_by)}
				LIMIT %s
				OFFSET %s
			"""
		else:
			query += f"""
				LIMIT 1
			"""
		
		return query