from typing import Any
from dataclasses import dataclass


@dataclass
class BaseModel:
	@staticmethod
	def get_key(table: str, column: str) -> str:
		return f"{table}_{column}_key"
	
	@staticmethod
	def get_fkey(table: str, column: str) -> str:
		return f"{table}_{column}_fkey"
