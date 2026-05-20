from enum import StrEnum


class ReturnStatus(StrEnum):
	CREATED = "created"
	CONFIRMED = "confirmed"
	IN_TRANSIT = "in_transit"
	FINISHED = "finished"