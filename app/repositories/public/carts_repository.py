import psycopg
from typing import ClassVar
from app.models.public.cart import Cart
from app.types.cart_type import CartType
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.selectable_mixin import SelectableMixin


class CartsRepository(
	BaseRepository,
	SelectableMixin[Cart]
):
	TABLE: ClassVar[str] = Cart.TABLE
	MODEL = Cart
	TABLE_COLUMNS = (
		Cart.COLUMN_ID,
		Cart.COLUMN_USER_ID,
		Cart.COLUMN_TYPE,
		Cart.COLUMN_CREATED_AT,
	)

	ORDER_BY = ((Cart.COLUMN_CREATED_AT, "DESC",),)

	@classmethod
	def create(
		cls,
		cur: psycopg.Cursor,
		user_id: int,
		type: CartType
	) -> int:
		return cls.execute_create(
			cur=cur,
			table=cls.TABLE,
			fields={
				Cart.COLUMN_USER_ID: user_id,
				Cart.COLUMN_TYPE: type
			},
			returning=Cart.COLUMN_ID
		)[Cart.COLUMN_ID]
	
	@classmethod
	def get_by_id(
		cls,
		cur: psycopg.Cursor,
		cart_id: int,
	) -> Cart | None:
		return cls.select(
			cur=cur,
			equals={Cart.COLUMN_ID: cart_id}
		)
	
	@classmethod
	def get_by_user_id_type(
		cls,
		cur: psycopg.Cursor,
		user_id: int,
		type: CartType
	) -> Cart | None:
		return cls.select(
			cur=cur,
			equals={Cart.COLUMN_USER_ID: user_id, Cart.COLUMN_TYPE: type}
		)
	
	@classmethod
	def get_many_by_user_id(
		cls,
		cur: psycopg.Cursor,
		user_id: int
	) -> list[Cart]:
		return cls.select_many(
			cur=cur,
			equals={Cart.COLUMN_USER_ID: user_id}
		)
