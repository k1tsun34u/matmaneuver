import psycopg
from typing import ClassVar
from decimal import Decimal
from app.models.public.order import Order
from app.types.payment_method import PaymentMethod
from app.models.public.order_payment import OrderPayment
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.selectable_mixin import SelectableMixin


class OrderPaymentsRepository(
	BaseRepository,
	SelectableMixin[OrderPayment]
):
	TABLE: ClassVar[str] = OrderPayment.TABLE
	MODEL = OrderPayment
	TABLE_COLUMNS = (
		OrderPayment.COLUMN_ID,
		OrderPayment.COLUMN_ORDER_ID,
		OrderPayment.COLUMN_AMOUNT,
		OrderPayment.COLUMN_PAYMENT_METHOD,
		OrderPayment.COLUMN_CREATED_AT,
	)

	ORDER_BY = ((OrderPayment.COLUMN_CREATED_AT, "DESC",),)

	@classmethod
	def create(
		cls,
		cur: psycopg.Cursor,
		order_id: int,
		amount: Decimal,
		payment_method: PaymentMethod
	) -> int:
		return cls.execute_create(
			cur=cur,
			table=cls.TABLE,
			fields={
				OrderPayment.COLUMN_ORDER_ID: order_id,
				OrderPayment.COLUMN_AMOUNT: amount,
				OrderPayment.COLUMN_PAYMENT_METHOD: payment_method
			},
			returning=OrderPayment.COLUMN_ID
		)[OrderPayment.COLUMN_ID]
	
	@classmethod
	def get_by_id(cls, cur: psycopg.Cursor, order_payment_id: int) -> OrderPayment | None:
		return cls.select(cur, {OrderPayment.COLUMN_ID: order_payment_id})

	@classmethod
	def get_many_by_order_id(
		cls,
		cur: psycopg.Cursor,
		order_id: int,
		limit: int = 50,
		offset: int = 0
	) -> list[OrderPayment]:
		return cls.select_many(
			cur=cur,
			equals={OrderPayment.COLUMN_ORDER_ID: order_id},
			limit=limit,
			offset=offset
		)
	
	@classmethod
	def get_total_paid_amount(
		cls,
		cur: psycopg.Cursor,
		order_id: int
	) -> Decimal:
		query = f"""
			SELECT COALESCE(
				SUM(op.{OrderPayment.COLUMN_AMOUNT}),
					0
			) AS total
			FROM {OrderPayment.TABLE} op
			WHERE op.{OrderPayment.COLUMN_ORDER_ID} = %s
		"""
		cur.execute(query, (order_id,))
		row = cur.fetchone()
		return Decimal(row["total"])
