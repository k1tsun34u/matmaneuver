from dataclasses import dataclass
from typing import Generic, TypeVar
from app.errors.base_error import BaseError


T = TypeVar("T")

@dataclass(slots=True)
class ServiceResult(Generic[T]):
	result: T | None = None
	error: BaseError | None = None
