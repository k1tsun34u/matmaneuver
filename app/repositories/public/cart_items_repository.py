from decimal import Decimal

import psycopg
from typing import ClassVar
from app.models.public.cart_item import CartItem
from app.models.public.product import Product
from app.types.delete_result import DeleteResult
from app.types.update_result import UpdateResult
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.selectable_mixin import SelectableMixin


class CartItemsRepository(
	BaseRepository,
	SelectableMixin[CartItem]
):
	TABLE: ClassVar[str] = CartItem.TABLE
	MODEL = CartItem
	TABLE_COLUMNS = (
		CartItem.COLUMN_CART_ID,
		CartItem.COLUMN_PRODUCT_ID,
		CartItem.COLUMN_QUANTITY,
		CartItem.COLUMN_CREATED_AT,
	)

	ORDER_BY = ((CartItem.COLUMN_CREATED_AT, "DESC",),)

	@classmethod
	def add_or_increment(
		cls,
		cur: psycopg.Cursor,
		cart_id: int,
		product_id: int
	) -> UpdateResult:
		query = f"""
			INSERT INTO {cls.TABLE} ({CartItem.COLUMN_CART_ID}, {CartItem.COLUMN_PRODUCT_ID}, {CartItem.COLUMN_QUANTITY})
			VALUES (%s, %s, 1)
			ON CONFLICT ({CartItem.COLUMN_CART_ID}, {CartItem.COLUMN_PRODUCT_ID})
			DO UPDATE SET {CartItem.COLUMN_QUANTITY} = cart_items.{CartItem.COLUMN_QUANTITY} + 1
		"""
		cur.execute(query, (cart_id, product_id,))
		if cur.rowcount != 0:
			return UpdateResult.SUCCESS
		return UpdateResult.FAIL_NOT_FOUND

	@classmethod
	def decrement_or_remove(
		cls,
		cur: psycopg.Cursor,
		cart_id: int,
		product_id: int
	) -> UpdateResult:
		update_query = f"""
			UPDATE {cls.TABLE}
			SET {CartItem.COLUMN_QUANTITY} = {CartItem.COLUMN_QUANTITY} - 1
			WHERE
				{CartItem.COLUMN_CART_ID} = %s
				AND {CartItem.COLUMN_PRODUCT_ID} = %s
				AND {CartItem.COLUMN_QUANTITY} > 1
		"""
		cur.execute(update_query, (cart_id, product_id,))
		if cur.rowcount != 0:
			return UpdateResult.SUCCESS
		
		delete_query = f"""
			DELETE FROM {cls.TABLE}
			WHERE
				{CartItem.COLUMN_CART_ID} = %s
				AND {CartItem.COLUMN_PRODUCT_ID} = %s
				AND {CartItem.COLUMN_QUANTITY} = 1
		"""
		cur.execute(delete_query, (cart_id, product_id,))
		if cur.rowcount != 0:
			return UpdateResult.SUCCESS
		return UpdateResult.FAIL_NOT_FOUND
	
	@classmethod
	def remove(
		cls,
		cur: psycopg.Cursor,
		cart_id: int,
		product_id: int
	) -> DeleteResult:
		rowcount = cls.execute_delete(
			cur=cur,
			table=cls.TABLE,
			where={CartItem.COLUMN_CART_ID: cart_id, CartItem.COLUMN_PRODUCT_ID: product_id}
		)

		if rowcount != 0:
			return DeleteResult.SUCCESS
		return DeleteResult.FAIL_NOT_FOUND
	
	@classmethod
	def delete_many_by_cart_id(
		cls,
		cur: psycopg.Cursor,
		cart_id: int
	) -> DeleteResult:
		rowcount = cls.execute_delete(
			cur=cur,
			table=cls.TABLE,
			where={CartItem.COLUMN_CART_ID: cart_id}
		)

		if rowcount != 0:
			return DeleteResult.SUCCESS
		
		# cart may not have any items
		return DeleteResult.SUCCESS
	
	@classmethod
	def get_by_cart_id_product_id(
		cls,
		cur: psycopg.Cursor,
		cart_id: int,
		product_id: int
	) -> CartItem | None:
		return cls.select(cur, {CartItem.COLUMN_CART_ID: cart_id, CartItem.COLUMN_PRODUCT_ID: product_id})
	
	@classmethod
	def get_many_by_cart_id(
		cls,
		cur: psycopg.Cursor,
		cart_id: int
	) -> list[CartItem]:
		return cls.select_many(
			cur=cur,
			equals={CartItem.COLUMN_CART_ID: cart_id}
		)

	@classmethod
	def get_total_price(
		cls,
		cur: psycopg.Cursor,
		cart_id: int
	) -> Decimal:
		query = f"""
			SELECT COALESCE(
				SUM(p.{Product.COLUMN_PRICE} * ci.{CartItem.COLUMN_QUANTITY}),
					0
			) AS total
			FROM {Product.TABLE} p
			JOIN
				{CartItem.TABLE} ci
				ON ci.{CartItem.COLUMN_PRODUCT_ID} = p.{Product.COLUMN_ID}
			WHERE
				ci.{CartItem.COLUMN_CART_ID} = %s
		"""
		cur.execute(query, (cart_id,))
		row = cur.fetchone()
		return Decimal(row["total"])
