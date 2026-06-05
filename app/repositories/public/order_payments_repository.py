import psycopg
from typing import ClassVar
from decimal import Decimal
from app.models.public.order import Order
from app.types.payment_method import PaymentMethod
from app.models.public.order_payment import OrderPayment
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.selectable_mixin import SelectableMixin
from app.utils import Utils


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
				OrderPayment.COLUMN_PAYMENT_METHOD: payment_method.value
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
	) -> tuple[list[OrderPayment], int]:
		payments = cls.select_many(
			cur=cur,
			equals={OrderPayment.COLUMN_ORDER_ID: order_id},
			limit=limit,
			offset=offset
		)

		query = f"""
			SELECT COUNT(*) AS total
			FROM {cls.TABLE}
			WHERE {OrderPayment.COLUMN_ORDER_ID} = %s
		"""
		cur.execute(query, (order_id,))
		return (payments, cur.fetchone()['total'],)

	@classmethod
	def get_many_by_user_id(
		cls,
		cur: psycopg.Cursor,
		user_id: int,
		limit: int = 50,
		offset: int = 0
	) -> tuple[list[OrderPayment], int]:
		query_part = f"""
			FROM {cls.TABLE} op
			JOIN {Order.TABLE} o ON o.{Order.COLUMN_ID} = op.{OrderPayment.COLUMN_ORDER_ID}
			WHERE o.{Order.COLUMN_CREATED_BY} = %s
		"""

		query = f"""
			SELECT op.*
			{query_part}
			{Utils.build_order_by(cls.ORDER_BY)}
			LIMIT %s
			OFFSET %s
		"""
		cur.execute(query, (user_id, limit, offset,))
		payments = [OrderPayment(**row) for row in cur.fetchall()]

		query = f"""
			SELECT COUNT(*) AS total
			{query_part}
		"""
		cur.execute(query, (user_id,))
		return (payments, cur.fetchone()['total'],)
	
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
