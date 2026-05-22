from dataclasses import dataclass


@dataclass
class TransactionHelper:
	entity: str
	"""example: 'User'"""

	table: str
	"""example: 'users'"""

	columns: tuple[str, ...]