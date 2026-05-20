from enum import StrEnum


class WriteOffReason(StrEnum):
	EXPIRED = "expired"
	DAMAGED = "damaged"
	LOST = "lost"
	STOLEN = "stolen"
	INVENTORY_MISMATCH = "inventory_mismatch"
	OTHER = "other"