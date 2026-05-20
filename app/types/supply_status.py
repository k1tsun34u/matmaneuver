from enum import StrEnum


class SupplyStatus(StrEnum):
	CREATED = "created"
	CONFIRMED = "confirmed"
	IN_TRANSIT = "in_transit"
	DELIVERED = "delivered"
	CANCELLED = "cancelled"