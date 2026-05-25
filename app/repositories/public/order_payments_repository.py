import psycopg
from decimal import Decimal
from app.types.payment_method import PaymentMethod
from app.models.public.order_payment import OrderPayment
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.selectable_mixin import SelectableMixin


class OrderPaymentsRepository(
	BaseRepository,
	SelectableMixin[OrderPayment]
):
	TABLE = "order_payments"
	MODEL = OrderPayment
	TABLE_COLUMNS = (
		"id",
		"order_id",
		"amount",
		"payment_method",
		"created_at",
	)

	ORDER_BY = (("created_at", "DESC",),)

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
				"order_id": order_id,
				"amount": amount,
				"payment_method": payment_method
			},
			returning="id"
		)["id"]
	
	@classmethod
	def get_by_id(cls, cur: psycopg.Cursor, order_payment_id: int) -> OrderPayment | None:
		return cls.select(cur, {"id": order_payment_id})

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
			equals={"order_id": order_id},
			limit=limit,
			offset=offset
		)
