import re
import random
import string
import psycopg
import marshmallow
from math import ceil
from datetime import date
from decimal import Decimal
from app.unset import Unset
from os.path import normpath
from typing import Any, Literal, TypeVar


T = TypeVar("T")

class MarshmallowEventSchema(marshmallow.Schema):
	event_date = marshmallow.fields.DateTime(required=True)


marshmallow_event_schema = MarshmallowEventSchema()


class Utils:
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
	
	@staticmethod
	def build_pagination_dict(
		offset: int,
		limit: int,
		page: int,
		items_name: str,
		total_items: int
	) -> str:
		return {
			'offset': offset,
			'limit': limit,
			'page': page,
			f'total_{items_name}': total_items,
			'total_pages': ceil(total_items / limit) if limit > 0 else 0
		}
	
	@staticmethod
	def page_to_limit_offset(page: int) -> tuple[int, int]:
		return (50, page * 50,)
	
	@staticmethod
	def normalize_pagination(limit: int, offset: int) -> tuple[int, int]:
		limit = max(1, min(limit, 100))
		offset = max(0, offset)
		return limit, offset

	@staticmethod
	def normalize_phone(phone: str) -> str:
		phone = re.sub(r'\D', '', phone)
		if len(phone) == 11 and phone.startswith('8'):
			phone = "7" + phone[1:]
		return phone

	@staticmethod
	def normalize_email(email: str) -> str:
		return email.lower()
	
	@staticmethod
	def normalize_full_name(full_name: str) -> str:
		return ' '.join(full_name.strip().split())
	
	@staticmethod
	def normalize_code(code: str) -> str:
		return code.strip().lower()
	
	@staticmethod
	def normalize_name(name: str) -> str:
		return name.strip()
	
	@staticmethod
	def normalize_storage_key(storage_key: str) -> str:
		return normpath(storage_key.strip())
	
	@staticmethod
	def normalize_track_number(track_number: str) -> str:
		return re.sub(r"[^\w-]", '', track_number.strip().upper())

	@staticmethod
	def is_valid_phone(normalized_phone: str) -> bool:
		return (
			normalized_phone
			and len(normalized_phone) == 11
			and normalized_phone.startswith('7')
			and normalized_phone.isdigit()
		)
	
	@staticmethod
	def is_valid_email(normalized_email: str) -> bool:
		pattern = r'^[a-z0-9._-]+@[a-z0-9.-]+\.[a-z]{2,}$'
		return (
			normalized_email
			and len(normalized_email) <= 256
			and bool(re.fullmatch(pattern, normalized_email))
		)

	@staticmethod
	def is_valid_full_name(normalized_full_name: str) -> bool:
		pattern = r"^[A-Za-zА-Яа-яЁё' -]+$"
		return (
			normalized_full_name
			and len(normalized_full_name) < 128
			and bool(re.fullmatch(pattern, normalized_full_name))
		)
	
	@staticmethod
	def is_valid_name(normalized_name: str) -> bool:
		pattern = r"^[\w\d ]+$"
		return (
			normalized_name
			and len(normalized_name) < 128
			and bool(re.fullmatch(pattern, normalized_name))
		)
	
	@staticmethod
	def is_valid_code(normalized_code: str) -> bool:
		pattern = r"^[a-z]+(?:_[a-z]+)*$"
		return (
			normalized_code
			and bool(re.fullmatch(pattern, normalized_code))
		)
	
	@staticmethod
	def is_valid_password_hash(password_hash: str) -> bool:
		return (
			password_hash
			and len(password_hash) > 0
		)
	
	@staticmethod
	def is_valid_storage_key(norm_storage_key: str) -> bool:
		pattern = r"^[a-zA-Z0-9_-]+"
		return (
			norm_storage_key
			and bool(re.fullmatch(pattern, norm_storage_key))
		)
	
	@staticmethod
	def is_valid_track_number(norm_track_number: str) -> bool:
		pattern = r"^\w+(?:-\w)*$"
		return (
			norm_track_number
			and bool(re.fullmatch(pattern, norm_track_number))
		)
	
	@classmethod
	def determine_result(
		cls,
		cur: psycopg.Cursor,
		table: str,
		where: dict[str, Any],
		rowcount: int,
		result_type: type[T]
	) -> T:
		if rowcount != 0:
			return result_type.SUCCESS

		conditions, params = cls.build_conditions_params(equals=where)
		query = f"""
			SELECT 1 FROM {table}
			{cls.build_where(conditions)}
		"""
		cur.execute(query, params)
		if not cur.fetchone():
			return result_type.FAIL_NOT_FOUND
		return result_type.FAIL_CONDITION
	
	@staticmethod
	def parse_str_from_dict(data: dict[str, Any], key: str) -> str | None:
		if not isinstance(data, dict):
			return None
		
		value = data.get(key)
		if not isinstance(value, str):
			return None
		
		return value
	
	@staticmethod
	def parse_int_from_dict(data: dict[str, Any], key: str) -> int | None:
		if not isinstance(data, dict):
			return None
		
		try:
			return int(data.get(key))
		except Exception:
			return None
	
	@staticmethod
	def parse_decimal_from_dict(data: dict[str, Any], key: str) -> Decimal | None:
		if not isinstance(data, dict):
			return None
		
		try:
			return Decimal(str(data.get(key)))
		except Exception:
			return None
	
	@staticmethod
	def parse_bool_from_dict(data: dict[str, Any], key: str) -> bool | None:
		if not isinstance(data, dict):
			return None
		
		value = data.get(key)
		if isinstance(value, bool):
			return value
		
		if isinstance(value, str):
			value = value.lower()
			if value in ("true", "1", "yes"):
				return True
			if value in ("false", "0", "no"):
				return False
		
		if isinstance(value, int):
			match value.lower():
				case '0':
					return False
				case '1':
					return True
		
		return None
	
	@staticmethod
	def parse_list_from_dict(data: dict[str, Any], key: str) -> list | None:
		if not isinstance(data, dict):
			return None
		
		value = data.get(key)
		if isinstance(value, list):
			return value
		
		return None
	
	@staticmethod
	def parse_str_enum_from_dict(data: dict[str, Any], key: str, result_type: type[T]) -> T | None:
		try:
			return result_type(Utils.parse_str_from_dict(data, key))
		except:
			return None
	
	@staticmethod
	def parse_enum_from_str(value: str, result_type: type[T]) -> T | None:
		try:
			return result_type(value)
		except:
			return None
	
	@staticmethod
	def parse_date_from_dict(data: dict[str, Any], key: str) -> date | None:
		try:
			s = Utils.parse_str_from_dict(data, key)
			if s is None:
				return None
			
			return marshmallow_event_schema.loads(s)
		except Exception:
			return None
	
	@staticmethod
	def gen_str(length: int, chars=string.ascii_uppercase + string.digits):
		return ''.join(random.choices(chars, k=length))
