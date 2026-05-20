from enum import StrEnum


class CartType(StrEnum):
	ACTIVE = "active"
	"""Активная корзина (для создания заказа)"""
	
	WISHLIST = "wishlist"
	"""Желаемое (для желаемых продуктов)"""
