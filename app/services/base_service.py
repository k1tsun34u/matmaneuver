
import logging
import psycopg.errors
from app.db import Db
from typing import ClassVar
from functools import wraps
from app.errors.base_error import BaseError
from app.models.public.base_model import BaseModel
from app.types.service_result import ServiceResult
from app.errors.unhandled_error import UnhandledError
from app.errors.not_found_error import NotFoundError
from app.types.transaction_helper import TransactionHelper
from app.errors.invalid_value_error import InvalidValueError
from typing import Callable, ParamSpec, TypeVar, Concatenate
from app.errors.already_exists_error import AlreadyExistsError


R = TypeVar("R")
P = ParamSpec("P")
logger = logging.getLogger(__name__)

class BaseService:
	KEY_HELPERS: ClassVar[tuple[TransactionHelper, ...]]
	FKEY_HELPERS: ClassVar[tuple[TransactionHelper, ...]]

	@classmethod
	def _map_constraint_to_error(
		cls,
		constraint: str,
		helpers: tuple[TransactionHelper, ...],
		column_converter: Callable[[str, str], str],
		builder: Callable[[str, str], BaseError],
		unhandled_violation: str
	) -> BaseError:
		for helper in helpers:
			for column in helper.columns:
				if constraint == column_converter(helper.table, column):
					return builder(helper.entity, column)
		logger.error(f"Unhandled {unhandled_violation} violation ('{constraint}')")
		return UnhandledError("Internal database error")

	@staticmethod
	def transaction(
		func: Callable[Concatenate[type, psycopg.Cursor, P], R]
	) -> Callable[Concatenate[type, P], R]:
		"""
			Requires class vars:
			- KEY_HELPERS: ClassVar[tuple[TransactionHelper, ...]]
			- FKEY_HELPERS: ClassVar[tuple[TransactionHelper, ...]]
		"""

		@wraps(func)
		def wrapper(cls, *args: P.args, **kwargs: P.kwargs) -> R:
			with Db.connection() as conn:
				try:
					with conn.cursor() as cur:
						result = func(cls, cur, *args, **kwargs)
					conn.commit()
					return result
				except Exception as e:
					conn.rollback()
					if isinstance(e, psycopg.errors.CheckViolation):
						logger.exception(f"Unhandled check violation", extra={"error": str(e)})

						# not good, but ok
						return ServiceResult(error=InvalidValueError("Constraint violation", e.diag.constraint_name))
					if isinstance(e, psycopg.errors.UniqueViolation):
						return ServiceResult(
							error=BaseService._map_constraint_to_error(
								constraint=e.diag.constraint_name,
								helpers=cls.KEY_HELPERS,
								column_converter=BaseModel.get_key,
								builder=AlreadyExistsError,
								unhandled_violation="unique"
							)
						)
					if isinstance(e, psycopg.errors.ForeignKeyViolation):
						return ServiceResult(
							error=BaseService._map_constraint_to_error(
								constraint=e.diag.constraint_name,
								helpers=cls.FKEY_HELPERS,
								column_converter=BaseModel.get_fkey,
								builder=NotFoundError,
								unhandled_violation="foreign key"
							)
						)

					logger.exception(f"Unhandled error", extra={"error": str(e)})
					raise
			
		return wrapper
