import psycopg
from app.utils import Utils
from typing import ClassVar
from app.models.public.order import Order
from app.types.order_status import OrderStatus
from app.types.update_result import UpdateResult
from datetime import date, datetime, time, timedelta
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.updatable_mixin import UpdatableMixin
from app.repositories.base.mixins.selectable_mixin import SelectableMixin


class OrdersRepository(
	BaseRepository,
	UpdatableMixin,
	SelectableMixin[Order]
):
	TABLE: ClassVar[str] = Order.TABLE
	MODEL = Order
	TABLE_COLUMNS = (
		Order.COLUMN_ID,
		Order.COLUMN_CURRENT_STATUS,
		Order.COLUMN_TRACK_NUMBER,
		Order.COLUMN_DELIVERY_ADDRESS,
		Order.COLUMN_CREATED_BY,
		Order.COLUMN_CREATED_AT,
	)

	ORDER_BY = ((Order.COLUMN_CREATED_AT, "DESC",),)

	@classmethod
	def create(
		cls,
		cur: psycopg.Cursor,
		track_number: str,
		delivery_address: str,
		created_by: int
	) -> int:
		return cls.execute_create(
			cur=cur,
			table=cls.TABLE,
			fields={
				Order.COLUMN_CURRENT_STATUS: OrderStatus.CREATED,
				Order.COLUMN_TRACK_NUMBER: track_number,
				Order.COLUMN_DELIVERY_ADDRESS: delivery_address,
				Order.COLUMN_CREATED_BY: created_by
			},
			returning=Order.COLUMN_ID
		)[Order.COLUMN_ID]
	
	@classmethod
	def set_status(
		cls,
		cur: psycopg.Cursor,
		order_id: int,
		status: OrderStatus
	) -> UpdateResult:
		return cls.update_by_conditions(
			cur=cur,
			identity_where={Order.COLUMN_ID: order_id},
			condition_where={},
			fields={Order.COLUMN_CURRENT_STATUS: status}
		)
	
	@classmethod
	def get_by_id(cls, cur: psycopg.Cursor, order_id: int) -> Order | None:
		return cls.select(cur, {Order.COLUMN_ID: order_id})
	
	@classmethod
	def get_by_id_for_update(
		cls,
		cur: psycopg.Cursor,
		order_id: int
	) -> Order | None:
		query = f"""
			SELECT {", ".join(cls.TABLE_COLUMNS)}
			FROM {cls.TABLE}
			WHERE {Order.COLUMN_ID} = %s
			FOR UPDATE
			LIMIT 1
		"""
		cur.execute(query, (order_id,))
		row = cur.fetchone()
		return Order(**row) if row else None
	
	@classmethod
	def get_by_track_number(cls, cur: psycopg.Cursor, track_number: str) -> Order | None:
		return cls.select(cur, {Order.COLUMN_TRACK_NUMBER: track_number})
	
	@classmethod
	def get_many_by_user_id(
		cls,
		cur: psycopg.Cursor,
		user_id: int,
		limit: int = 50,
		offset: int = 0
	) -> tuple[list[Order], int]:
		orders = cls.select_many(
			cur=cur,
			equals={Order.COLUMN_CREATED_BY: user_id},
			limit=limit,
			offset=offset
		)
	
		query = f"""
			SELECT COUNT(*) AS total
			FROM {cls.TABLE}
			WHERE {Order.COLUMN_CREATED_BY} = %s
		"""
		cur.execute(query, (user_id,))
		return (orders, cur.fetchone()['total'],)
	
	@classmethod
	def search(
		cls,
		cur: psycopg.Cursor,
		search: str | None = None,
		status: OrderStatus | None = None,
		created_from: date | None = None,
		created_to: date | None = None,
		limit: int = 50,
		offset: int = 0
	) -> tuple[list[Order], int]:
		limit, offset = Utils.normalize_pagination(limit, offset)
		conditions = []
		params = []
		if search is not None:
			conditions.append(f"({Order.COLUMN_TRACK_NUMBER} ILIKE %s OR {Order.COLUMN_DELIVERY_ADDRESS} ILIKE %s)")
			params.append(f"%{search}%")
			params.append(f"%{search}%")
		if status is not None:
			conditions.append(f"{Order.COLUMN_CURRENT_STATUS} = %s")
			params.append(status)
		if created_from is not None:
			conditions.append(f"{Order.COLUMN_CREATED_AT} >= %s")
			params.append(datetime.combine(created_from, time.min))
		if created_to is not None:
			conditions.append(f"{Order.COLUMN_CREATED_AT} < %s")
			params.append(datetime.combine(created_to + timedelta(days=1), time.min))
		
		query = Utils.build_select_statement(
			select_fields=cls.TABLE_COLUMNS,
			table=cls.TABLE,
			conditions=tuple(conditions),
			order_by=cls.ORDER_BY,
			many=True
		)

		cur.execute(query, (*params, limit, offset,))
		orders = [Order(**row) for row in cur.fetchall()]

		query = f"""
			SELECT COUNT(*) AS total
			FROM {cls.TABLE}
			{Utils.build_where(conditions)}
		"""
		cur.execute(query, params)
		return (orders, cur.fetchone()['total'],)
