import psycopg
from datetime import date
from app.utils import Utils
from app.models.public.order import Order
from app.models.public.product import Product
from app.types.order_status import OrderStatus
from app.types.update_result import UpdateResult
from app.types.delete_result import DeleteResult
from app.services.base_service import BaseService
from app.types.service_result import ServiceResult
from app.models.public.order_item import OrderItem
from app.errors.not_found_error import NotFoundError
from app.types.permission_code import PermissionCode
from app.errors.not_allowed_error import NotAllowedError
from app.types.transaction_helper import TransactionHelper
from app.errors.invalid_value_error import InvalidValueError
from app.models.public.order_status_history import OrderStatusHistory
from app.repositories.public.orders_repository import OrdersRepository
from app.repositories.public.products_repository import ProductsRepository
from app.repositories.public.order_items_repository import OrderItemsRepository
from app.repositories.public.order_status_history_repository import OrderStatusHistoryRepository as OSHR
from app.repositories.public.employee_permissions_repository import EmployeePermissionsRepository as EPR


class OrdersService(BaseService):
	KEY_HELPERS = (TransactionHelper(Order.ENTITY, Order.TABLE, (Order.COLUMN_TRACK_NUMBER,)),)
	FKEY_HELPERS = (
		TransactionHelper(Order.ENTITY, Order.TABLE, (Order.COLUMN_CREATED_BY,)),
		TransactionHelper(OrderItem.ENTITY, OrderItem.TABLE, (
			OrderItem.COLUMN_ORDER_ID,
			OrderItem.COLUMN_PRODUCT_ID,
		)),
		TransactionHelper(OrderStatusHistory.ENTITY, OrderStatusHistory.TABLE, (
			OrderStatusHistory.COLUMN_ORDER_ID,
			OrderStatusHistory.COLUMN_CHANGED_BY,
		)),
	)

	ALLOWED_STATUS_TRANSITIONS = {
		OrderStatus.CREATED: (OrderStatus.CONFIRMED, OrderStatus.CANCELLED,),
		OrderStatus.CONFIRMED: (OrderStatus.IN_TRANSIT, OrderStatus.CANCELLED,),
		OrderStatus.IN_TRANSIT: (OrderStatus.DELIVERED,),
		OrderStatus.DELIVERED: tuple(),
		OrderStatus.CANCELLED: tuple()
	}

	ALLOWED_ITEM_EDIT_STATUSES = (OrderStatus.CREATED,)

	@classmethod
	@BaseService.transaction
	def create(
		cls,
		cur: psycopg.Cursor,
		track_number: str,
		delivery_address: str,
		created_by: int
	) -> ServiceResult:
		"""
			Args:
				created_by (int): users(id)
			Errors:
			- InvalidValueError
			- AlreadyExistsError
			- NotFoundError
			- UnhandledError
		"""

		norm_track_number = Utils.normalize_track_number(track_number)
		if not Utils.is_valid_track_number(norm_track_number):
			return ServiceResult(error=InvalidValueError(Order.ENTITY, Order.COLUMN_TRACK_NUMBER))
		
		order_id = OrdersRepository.create(
			cur=cur,
			track_number=norm_track_number,
			delivery_address=delivery_address,
			created_by=created_by
		)

		latest_status_id = OSHR.create(cur, order_id, OrderStatus.CREATED, created_by)
		return ServiceResult(result=(order_id, latest_status_id,))
	
	@classmethod
	@BaseService.transaction
	def set_status(
		cls,
		cur: psycopg.Cursor,
		order_id: int,
		status: OrderStatus,
		set_by: int | None
	) -> ServiceResult:
		"""
			Args:
				set_by (int | None): employees(id)
			Errors:
			- NotAllowedError
			- NotFoundError
			- InvalidValueError
			- UnhandledError
		"""

		if set_by is not None and not EPR.has_permission(cur, set_by, PermissionCode.SET_ORDER_STATUS):
			return ServiceResult(error=NotAllowedError(PermissionCode.SET_ORDER_STATUS, Order.COLUMN_CURRENT_STATUS))
		
		order = OrdersRepository.get_by_id_for_update(cur, order_id)
		if order is None:
			return ServiceResult(error=NotFoundError(Order.ENTITY, Order.COLUMN_ID))
		
		if status not in cls.ALLOWED_STATUS_TRANSITIONS[order.current_status]:
			return ServiceResult(error=InvalidValueError(Order.ENTITY, Order.COLUMN_CURRENT_STATUS))
		
		changed = OrdersRepository.set_status(
			cur=cur,
			order_id=order_id,
			status=status
		)

		if changed == UpdateResult.FAIL_NOT_FOUND:
			return ServiceResult(error=NotFoundError(Order.ENTITY, Order.COLUMN_ID))
		return ServiceResult(result=OSHR.create(cur, order_id, status, set_by))
	
	@classmethod
	@BaseService.transaction
	def get_by_id(
		cls,
		cur: psycopg.Cursor,
		order_id: int
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- UnhandledError
		"""

		order = OrdersRepository.get_by_id(cur, order_id)
		if not order:
			return ServiceResult(error=NotFoundError(Order.ENTITY, Order.COLUMN_ID))
		return ServiceResult(result=order)
	
	@classmethod
	@BaseService.transaction
	def get_by_track_number(
		cls,
		cur: psycopg.Cursor,
		track_number: str
	) -> ServiceResult:
		"""
			Errors:
			- InvalidValueError
			- NotFoundError
			- UnhandledError
		"""

		norm_track_number = Utils.normalize_track_number(track_number)
		if not Utils.is_valid_track_number(norm_track_number):
			return ServiceResult(error=InvalidValueError(Order.ENTITY, Order.COLUMN_TRACK_NUMBER))

		order = OrdersRepository.get_by_track_number(cur, norm_track_number)
		if not order:
			return ServiceResult(error=NotFoundError(Order.ENTITY, Order.COLUMN_TRACK_NUMBER))
		return ServiceResult(result=order)
	
	@classmethod
	@BaseService.transaction
	def get_many_by_user_id(
		cls,
		cur: psycopg.Cursor,
		user_id: int,
		limit: int = 50,
		offset: int = 0
	) -> ServiceResult:
		return ServiceResult(
			result=OrdersRepository.get_many_by_user_id(
				cur=cur,
				user_id=user_id,
				limit=limit,
				offset=offset
			)
		)
	
	@classmethod
	@BaseService.transaction
	def search(
		cls,
		cur: psycopg.Cursor,
		search: str | None = None,
		user_id: int | None = None,
		status: OrderStatus | None = None,
		created_from: date | None = None,
		created_to: date | None = None,
		limit: int = 50,
		offset: int = 0
	) -> ServiceResult:
		"""
			Errors:
			- UnhandledError
		"""

		return ServiceResult(
			result=OrdersRepository.search(
				cur=cur,
				search=search,
				user_id=user_id,
				status=status,
				created_from=created_from,
				created_to=created_to,
				limit=limit,
				offset=offset
			)
		)

	@classmethod
	@BaseService.transaction
	def create_item(
		cls,
		cur: psycopg.Cursor,
		order_id: int,
		product_id: int,
		quantity: int
	) -> ServiceResult:
		"""
			Errors:
			- InvalidValueError
			- AlreadyExistsError
			- NotFoundError
			- UnhandledError
		"""
		
		order = OrdersRepository.get_by_id_for_update(cur, order_id)
		if order is None:
			return ServiceResult(error=NotFoundError(Order.ENTITY, Order.COLUMN_ID))
		
		if order.current_status not in cls.ALLOWED_ITEM_EDIT_STATUSES:
			return ServiceResult(error=InvalidValueError(Order.ENTITY, Order.COLUMN_CURRENT_STATUS))
		
		product = ProductsRepository.get_by_id(cur, product_id)
		if product is None:
			return ServiceResult(error=NotFoundError(Product.ENTITY, Product.COLUMN_ID))
		
		return ServiceResult(
			result=OrderItemsRepository.create(
				cur=cur,
				order_id=order_id,
				product_id=product_id,
				quantity=quantity,
				price=product.price
			)
		)
	
	@classmethod
	@BaseService.transaction
	def delete_item(
		cls,
		cur: psycopg.Cursor,
		order_item_id: int
	) -> ServiceResult:
		"""
			Errors:
			- InvalidValueError
			- NotFoundError
			- UnhandledError
		"""
		
		order_item = OrderItemsRepository.get_by_id(cur, order_item_id)
		if order_item is None:
			return ServiceResult(error=NotFoundError(OrderItem.ENTITY, OrderItem.COLUMN_ID))
		
		order = OrdersRepository.get_by_id_for_update(cur, order_item.order_id)
		if order is None:
			return ServiceResult(error=NotFoundError(Order.ENTITY, Order.COLUMN_ID))
		
		if order.current_status not in cls.ALLOWED_ITEM_EDIT_STATUSES:
			return ServiceResult(error=InvalidValueError(Order.ENTITY, Order.COLUMN_CURRENT_STATUS))

		if OrderItemsRepository.delete(cur, order_item_id) == DeleteResult.FAIL_NOT_FOUND:
			return ServiceResult(error=NotFoundError(OrderItem.ENTITY, OrderItem.COLUMN_ID))
		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def get_item_by_id(
		cls,
		cur: psycopg.Cursor,
		order_item_id: int
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- UnhandledError
		"""

		order_item = OrderItemsRepository.get_by_id(cur, order_item_id)
		if not order_item:
			return ServiceResult(error=NotFoundError(OrderItem.ENTITY, OrderItem.COLUMN_ID))
		return ServiceResult(result=order_item)
	
	@classmethod
	@BaseService.transaction
	def get_items_by_order_id(
		cls,
		cur: psycopg.Cursor,
		order_id: int,
		limit: int | None = 50,
		offset: int = 0
	) -> ServiceResult:
		"""
			Errors:
			- UnhandledError
		"""

		return ServiceResult(
			result=OrderItemsRepository.get_many_by_order_id(
				cur=cur,
				order_id=order_id,
				limit=limit,
				offset=offset
			)
		)
	
	@classmethod
	@BaseService.transaction
	def get_items_by_product_id(
		cls,
		cur: psycopg.Cursor,
		product_id: int,
		limit: int = 50,
		offset: int = 0
	) -> ServiceResult:
		"""
			Errors:
			- UnhandledError
		"""

		return ServiceResult(
			result=OrderItemsRepository.get_many_by_product_id(
				cur=cur,
				product_id=product_id,
				limit=limit,
				offset=offset
			)
		)
	
	@classmethod
	@BaseService.transaction
	def get_total_price(
		cls,
		cur: psycopg.Cursor,
		order_id: int
	) -> ServiceResult:
		return ServiceResult(
			result=OrderItemsRepository.get_total_price(
				cur=cur,
				order_id=order_id
			)
		)
	
	@classmethod
	@BaseService.transaction
	def get_status_history(
		cls,
		cur: psycopg.Cursor,
		order_id: int,
		limit: int = 50,
		offset: int = 0
	) -> ServiceResult:
		"""
			Errors:
			- UnhandledError
		"""

		return ServiceResult(
			result=OSHR.get_many_by_order_id(
				cur=cur,
				order_id=order_id,
				limit=limit,
				offset=offset
			)
		)
