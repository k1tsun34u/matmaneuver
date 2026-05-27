import psycopg
from app.models.public.cart import Cart
from app.types.cart_type import CartType
from app.models.public.cart_item import CartItem
from app.types.update_result import UpdateResult
from app.types.delete_result import DeleteResult
from app.services.base_service import BaseService
from app.types.service_result import ServiceResult
from app.errors.not_found_error import NotFoundError
from app.types.transaction_helper import TransactionHelper
from app.repositories.public.carts_repository import CartsRepository
from app.repositories.public.cart_items_repository import CartItemsRepository


class CartsService(BaseService):
	KEY_HELPERS = tuple()
	FKEY_HELPERS = (
		TransactionHelper(Cart.ENTITY, Cart.TABLE, (Cart.COLUMN_USER_ID,)),
		TransactionHelper(CartItem.ENTITY, CartItem.TABLE, (
			CartItem.COLUMN_CART_ID,
			CartItem.COLUMN_PRODUCT_ID,
		)),
	)

	@classmethod
	@BaseService.transaction
	def create(
		cls,
		cur: psycopg.Cursor,
		user_id: int,
		type: CartType
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- UnhandledError
		"""

		return ServiceResult(result=CartsRepository.create(cur, user_id, type))
	
	@classmethod
	@BaseService.transaction
	def get_by_id(
		cls,
		cur: psycopg.Cursor,
		cart_id: int,
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- UnhandledError
		"""

		cart = CartsRepository.get_by_id(cur, cart_id)
		if cart is None:
			return ServiceResult(error=NotFoundError(Cart.ENTITY, Cart.COLUMN_ID))
		return ServiceResult(result=cart)
	
	@classmethod
	@BaseService.transaction
	def get_by_user_id_type(
		cls,
		cur: psycopg.Cursor,
		user_id: int,
		type: CartType
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- UnhandledError
		"""

		cart = CartsRepository.get_by_user_id_type(cur, user_id, type)
		if cart is None:
			return ServiceResult(error=NotFoundError(Cart.ENTITY, Cart.COLUMN_TYPE))
		return ServiceResult(result=cart)
	
	@classmethod
	@BaseService.transaction
	def get_many_by_user_id(
		cls,
		cur: psycopg.Cursor,
		user_id: int
	) -> ServiceResult:
		"""
			Errors:
			- UnhandledError
		"""

		return ServiceResult(result=CartsRepository.get_many_by_user_id(cur, user_id))

	@classmethod
	@BaseService.transaction
	def add_item_or_increment(
		cls,
		cur: psycopg.Cursor,
		cart_id: int,
		product_id: int
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- UnhandledError
		"""

		if CartItemsRepository.add_or_increment(cur, cart_id, product_id) == UpdateResult.FAIL_NOT_FOUND:
			return ServiceResult(error=NotFoundError(CartItem.ENTITY, CartItem.COLUMN_PRODUCT_ID))
		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def decrement_item_or_remove(
		cls,
		cur: psycopg.Cursor,
		cart_id: int,
		product_id: int
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- UnhandledError
		"""

		if CartItemsRepository.decrement_or_remove(cur, cart_id, product_id) == UpdateResult.FAIL_NOT_FOUND:
			return ServiceResult(error=NotFoundError(CartItem.ENTITY, CartItem.COLUMN_PRODUCT_ID))
		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def remove_item(
		cls,
		cur: psycopg.Cursor,
		cart_id: int,
		product_id: int
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- UnhandledError
		"""
		
		if CartItemsRepository.remove(cur, cart_id, product_id) == DeleteResult.FAIL_NOT_FOUND:
			return ServiceResult(error=NotFoundError(CartItem.ENTITY, CartItem.COLUMN_PRODUCT_ID))
		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def delete_items_by_cart_id(
		cls,
		cur: psycopg.Cursor,
		cart_id: int
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- UnhandledError
		"""
		
		if CartItemsRepository.delete_many_by_cart_id(cur, cart_id) == DeleteResult.FAIL_NOT_FOUND:
			return ServiceResult(error=NotFoundError(CartItem.ENTITY, CartItem.COLUMN_CART_ID))
		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def get_item_by_cart_id_product_id(
		cls,
		cur: psycopg.Cursor,
		cart_id: int,
		product_id: int
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- UnhandledError
		"""
		
		cart_item = CartItemsRepository.get_by_cart_id_product_id(cur, cart_id, product_id)
		if cart_item is None:
			return ServiceResult(error=NotFoundError(CartItem.ENTITY, CartItem.COLUMN_PRODUCT_ID))
		return ServiceResult(result=cart_item)
	
	@classmethod
	@BaseService.transaction
	def get_items_by_cart_id(
		cls,
		cur: psycopg.Cursor,
		cart_id: int
	) -> ServiceResult:
		"""
			Errors:
			- UnhandledError
		"""
		
		return ServiceResult(result=CartItemsRepository.get_many_by_cart_id(cur, cart_id))
