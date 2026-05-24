from enum import IntEnum


class DeleteResult(IntEnum):
	SUCCESS = 0
	FAIL_NOT_FOUND = 1
	FAIL_CONDITION = 2
