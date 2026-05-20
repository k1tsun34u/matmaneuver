import psycopg
from app.models.public.cart import Cart
from app.types.cart_type import CartType
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.selectable_mixin import SelectableMixin


class CartsRepository(
	BaseRepository,
	SelectableMixin[Cart]
):
	TABLE = "carts"
	MODEL = Cart
	SELECT_FIELDS = (
		"id",
		"user_id",
		"type",
		"created_at",
	)

	ORDER_BY = (("created_at", "DESC"),)

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
				"user_id": user_id,
				"type": type
			},
			returning="id"
		)["id"]
	
	@classmethod
	def get_many_by_user_id(
		cls,
		cur: psycopg.Cursor,
		user_id: int
	) -> list[Cart]:
		return cls.select_many(
			cur=cur,
			equals={"user_id": user_id}
		)
