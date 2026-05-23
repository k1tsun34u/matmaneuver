from enum import IntEnum


class DeactivateResult(IntEnum):
	SUCCESS = 0
	FAIL_NOT_FOUND = 1
	FAIL_IS_SYSTEM = 2
