import psycopg
from app.models.public.cart_item import CartItem
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.selectable_mixin import SelectableMixin


class CartItemsRepository(
	BaseRepository,
	SelectableMixin[CartItem]
):
	TABLE = "cart_items"
	MODEL = CartItem
	TABLE_COLUMNS = (
		"cart_id",
		"product_id",
		"quantity",
		"created_at",
	)

	ORDER_BY = (("created_at", "DESC",),)

	@classmethod
	def add_or_increment(
		cls,
		cur: psycopg.Cursor,
		cart_id: int,
		product_id: int
	) -> int:
		query = f"""
			INSERT INTO {cls.TABLE} (cart_id, product_id, quantity)
			VALUES (%s, %s, 1)
			ON CONFLICT (cart_id, product_id)
			DO UPDATE SET quantity = cart_items.quantity + 1
		"""
		cur.execute(query, (cart_id, product_id,))
		return cur.rowcount

	@classmethod
	def decrement(
		cls,
		cur: psycopg.Cursor,
		cart_id: int,
		product_id: int
	) -> int:
		update_query = f"""
			UPDATE {cls.TABLE}
			SET quantity = quantity - 1
			WHERE
				cart_id = %s AND product_id = %s
				AND quantity > 0
		"""
		cur.execute(update_query, (cart_id, product_id,))
		return cur.rowcount
	
	@classmethod
	def remove(
		cls,
		cur: psycopg.Cursor,
		cart_id: int,
		product_id: int
	) -> int:
		return cls.execute_delete(
			cur=cur,
			table=cls.TABLE,
			where={"cart_id": cart_id, "product_id": product_id}
		)
	
	@classmethod
	def get_by_cart_id_product_id(
		cls,
		cur: psycopg.Cursor,
		cart_id: int,
		product_id: int
	) -> CartItem | None:
		return cls.select(cur, {"cart_id": cart_id, "product_id": product_id})
	
	@classmethod
	def get_many_by_cart_id(
		cls,
		cur: psycopg.Cursor,
		cart_id: int
	) -> list[CartItem]:
		return cls.select_many(
			cur=cur,
			equals={"cart_id": cart_id}
		)
