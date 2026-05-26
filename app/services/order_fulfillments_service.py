import psycopg
from app.models.public.order import Order
from app.services.base_service import BaseService
from app.types.order_status import OrderStatus
from app.types.service_result import ServiceResult
from app.errors.not_found_error import NotFoundError
from app.types.transaction_helper import TransactionHelper
from app.errors.invalid_value_error import InvalidValueError
from app.models.public.order_fulfillment import OrderFulfillment
from app.repositories.public.orders_repository import OrdersRepository
from app.models.public.order_fulfillment_item import OrderFulfillmentItem
from app.repositories.public.order_items_repository import OrderItemsRepository
from app.repositories.public.order_fulfillments_repository import OrderFulfillmentsRepository as OFR
from app.repositories.public.order_fulfillment_items_repository import OrderFulfillmentItemsRepository as OFIR


class OrderFulfillmentsService(BaseService):
	KEY_HELPERS = tuple()
	FKEY_HELPERS = (
		TransactionHelper(OrderFulfillment.ENTITY, OrderFulfillment.TABLE, (
			OrderFulfillment.COLUMN_ORDER_ID,
			OrderFulfillment.COLUMN_WAREHOUSE_ID,
		)),
		TransactionHelper(OrderFulfillmentItem.ENTITY, OrderFulfillmentItem.TABLE, (
			OrderFulfillmentItem.COLUMN_ORDER_FULFILLMENT_ID,
			OrderFulfillmentItem.COLUMN_PRODUCT_ID,
		)),
	)

	ALLOWED_FULFILLMENT_STATUSES = (OrderStatus.CONFIRMED,)

	@classmethod
	@BaseService.transaction
	def create(
		cls,
		cur: psycopg.Cursor,
		order_id: int,
		warehouse_id: int
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- InvalidValueError
			- UnhandledError
		"""

		order = OrdersRepository.get_by_id_for_update(cur, order_id)
		if order is None:
			return ServiceResult(error=NotFoundError(Order.ENTITY, Order.COLUMN_ID))
		
		if order.current_status not in cls.ALLOWED_FULFILLMENT_STATUSES:
			return ServiceResult(error=InvalidValueError(Order.ENTITY, Order.COLUMN_CURRENT_STATUS))
		
		order_fulfillment_id = OFR.create(
			cur=cur,
			order_id=order_id,
			warehouse_id=warehouse_id
		)

		return ServiceResult(result=order_fulfillment_id)
	
	@classmethod
	@BaseService.transaction
	def get_by_id(
		cls,
		cur: psycopg.Cursor,
		order_fulfillment_id: int
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- UnhandledError
		"""

		order_fulfillment = OFR.get_by_id(cur, order_fulfillment_id)
		if not order_fulfillment:
			return ServiceResult(error=NotFoundError(OrderFulfillment.ENTITY, OrderFulfillment.COLUMN_ID))
		return ServiceResult(result=order_fulfillment)
	
	@classmethod
	@BaseService.transaction
	def get_many_by_order_id(
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
			result=OFR.get_many_by_order_id(
				cur=cur,
				order_id=order_id,
				limit=limit,
				offset=offset
			)
		)
	
	@classmethod
	@BaseService.transaction
	def get_many_by_warehouse_id(
		cls,
		cur: psycopg.Cursor,
		warehouse_id: int,
		limit: int = 50,
		offset: int = 0
	) -> ServiceResult:
		"""
			Errors:
			- UnhandledError
		"""

		return ServiceResult(
			result=OFR.get_many_by_warehouse_id(
				cur=cur,
				warehouse_id=warehouse_id,
				limit=limit,
				offset=offset
			)
		)

	@classmethod
	@BaseService.transaction
	def create_item(
		cls,
		cur: psycopg.Cursor,
		order_fulfillment_id: int,
		product_id: int,
		quantity: int
	) -> ServiceResult:
		"""
			Errors:
			- AlreadyExistsError
			- NotFoundError
			- UnhandledError
		"""
		
		order_fulfillment = OFR.get_by_id_for_update(cur, order_fulfillment_id)
		if order_fulfillment is None:
			return ServiceResult(error=NotFoundError(OrderFulfillment.ENTITY, OrderFulfillment.COLUMN_ID))
		
		order = OrdersRepository.get_by_id_for_update(cur, order_fulfillment.order_id)
		if order is None:
			return ServiceResult(error=NotFoundError(Order.ENTITY, Order.COLUMN_ID))
		
		if order.current_status not in cls.ALLOWED_FULFILLMENT_STATUSES:
			return ServiceResult(error=InvalidValueError(Order.ENTITY, Order.COLUMN_CURRENT_STATUS))
		
		order_item = OrderItemsRepository.get_by_order_id_product_id(cur, order.id, product_id)
		if order_item is None:
			return ServiceResult(error=InvalidValueError(OrderFulfillmentItem.ENTITY, OrderFulfillmentItem.COLUMN_PRODUCT_ID))
		
		if quantity > order_item.quantity:
			return ServiceResult(error=InvalidValueError(OrderFulfillmentItem.ENTITY, OrderFulfillmentItem.COLUMN_QUANTITY))

		already_fulfilled = OFIR.get_total_fulfilled_quantity(
			cur=cur,
			order_id=order.id,
			product_id=product_id
		)

		if already_fulfilled + quantity > order_item.quantity:
			return ServiceResult(
				error=InvalidValueError(
					OrderFulfillmentItem.ENTITY,
					OrderFulfillmentItem.COLUMN_QUANTITY
				)
			)

		return ServiceResult(
			result=OFIR.create(
				cur=cur,
				order_fulfillment_id=order_fulfillment_id,
				product_id=product_id,
				quantity=quantity,
				price=order_item.price
			)
		)
	
	@classmethod
	@BaseService.transaction
	def get_item_by_id(
		cls,
		cur: psycopg.Cursor,
		order_fulfillment_item_id: int
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- UnhandledError
		"""

		order_fulfillment_item = OFIR.get_by_id(cur, order_fulfillment_item_id)
		if not order_fulfillment_item:
			return ServiceResult(error=NotFoundError(OrderFulfillmentItem.ENTITY, OrderFulfillmentItem.COLUMN_ID))
		return ServiceResult(result=order_fulfillment_item)
	
	@classmethod
	@BaseService.transaction
	def get_items_by_order_fulfillment_id(
		cls,
		cur: psycopg.Cursor,
		order_fulfillment_id: int,
		limit: int = 50,
		offset: int = 0
	) -> ServiceResult:
		"""
			Errors:
			- UnhandledError
		"""

		return ServiceResult(
			result=OFIR.get_many_by_order_fulfillment_id(
				cur=cur,
				order_fulfillment_id=order_fulfillment_id,
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
			result=OFIR.get_many_by_product_id(
				cur=cur,
				product_id=product_id,
				limit=limit,
				offset=offset
			)
		)
