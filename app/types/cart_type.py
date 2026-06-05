from enum import StrEnum


class CartType(StrEnum):
	ACTIVE = "ACTIVE"
	"""Активная корзина (для создания заказа)"""
	
	WISHLIST = "WISHLIST"
	"""Желаемое (для желаемых продуктов)"""
