import psycopg
from decimal import Decimal
from app.models.public.order import Order
from app.models.public.order_item import OrderItem
from app.repositories.public.order_items_repository import OrderItemsRepository
from app.repositories.public.orders_repository import OrdersRepository
from app.types.order_status import OrderStatus
from app.services.base_service import BaseService
from app.types.payment_method import PaymentMethod
from app.types.service_result import ServiceResult
from app.errors.not_found_error import NotFoundError
from app.models.public.order_payment import OrderPayment
from app.types.transaction_helper import TransactionHelper
from app.errors.invalid_value_error import InvalidValueError
from app.repositories.public.order_payments_repository import OrderPaymentsRepository


class OrderPaymentsService(BaseService):
	KEY_HELPERS = tuple()
	FKEY_HELPERS = (TransactionHelper(OrderPayment.ENTITY, OrderPayment.TABLE, (OrderPayment.COLUMN_ORDER_ID,)),)

	ALLOWED_PAYMENT_STATUSES = (OrderStatus.CREATED,)

	@classmethod
	@BaseService.transaction
	def create(
		cls,
		cur: psycopg.Cursor,
		order_id: int,
		amount: Decimal,
		payment_method: PaymentMethod
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
		
		if order.current_status not in cls.ALLOWED_PAYMENT_STATUSES:
			return ServiceResult(error=InvalidValueError(Order.ENTITY, Order.COLUMN_CURRENT_STATUS))
		
		total_price = OrderItemsRepository.get_total_price(cur, order_id)
		if total_price <= 0:
			return ServiceResult(error=InvalidValueError(OrderItem.ENTITY, OrderItem.COLUMN_PRICE))
		
		already_paid = OrderPaymentsRepository.get_total_paid_amount(cur, order_id)
		if already_paid + amount > total_price:
			return ServiceResult(error=InvalidValueError(OrderPayment.ENTITY, OrderPayment.COLUMN_AMOUNT))
		
		order_payment_id = OrderPaymentsRepository.create(
			cur=cur,
			order_id=order_id,
			amount=amount,
			payment_method=payment_method
		)

		return ServiceResult(result=order_payment_id)
	
	@classmethod
	@BaseService.transaction
	def get_by_id(
		cls,
		cur: psycopg.Cursor,
		order_payment_id: int
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- UnhandledError
		"""

		order_payment = OrderPaymentsRepository.get_by_id(cur, order_payment_id)
		if not order_payment:
			return ServiceResult(error=NotFoundError(OrderPayment.ENTITY, OrderPayment.COLUMN_ID))
		return ServiceResult(result=order_payment)
	
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
			result=OrderPaymentsRepository.get_many_by_order_id(
				cur=cur,
				order_id=order_id,
				limit=limit,
				offset=offset
			)
		)
	
	@classmethod
	@BaseService.transaction
	def is_fully_paid(
		cls,
		cur: psycopg.Cursor,
		order_id: int
	) -> ServiceResult:
		"""
			Errors:
			- InvalidValueError
			- UnhandledError
		"""
		total_price = OrderItemsRepository.get_total_price(cur, order_id)
		if total_price <= 0:
			return ServiceResult(error=InvalidValueError(OrderItem.ENTITY, OrderItem.COLUMN_PRICE))

		already_paid = OrderPaymentsRepository.get_total_paid_amount(cur, order_id)
		return ServiceResult(result=already_paid >= total_price)
