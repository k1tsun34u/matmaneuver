from enum import StrEnum


class PaymentMethod(StrEnum):
	CASH = "CASH"
	"""Наличные"""

	CARD = "CARD"
	"""Банковская карта"""

	SBP = "SBP"
	"""Система Быстрых Платежей"""
