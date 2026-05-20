from enum import StrEnum


class PaymentMethod(StrEnum):
	CASH = "cash"
	"""Наличные"""

	CARD = "card"
	"""Банковская карта"""

	SBP = "sbp"
	"""Система Быстрых Платежей"""
