from app.utils import Utils
from datetime import datetime
from dataclasses import asdict
from app.errors.mapper import Mapper
from app.types.cart_type import CartType
from flask import Blueprint, jsonify, request
from app.types.order_status import OrderStatus
from app.session_manager import require_session
from app.types.payment_method import PaymentMethod
from app.services.carts_service import CartsService
from app.services.orders_service import OrdersService
from app.dtos.api.client.response_order import ResponseOrder
from app.services.order_payments_service import OrderPaymentsService


client_orders_bp = Blueprint(
	"api_client_orders",
	__name__,
	url_prefix="/api/client/orders"
)

@client_orders_bp.post('/create')
@require_session
def create(_, token):
	data = request.get_json()
	delivery_address = Utils.parse_str_from_dict(data, 'delivery_address')
	if delivery_address is None:
		return Mapper.router_error('Неверный запрос!', 400)

	tmp = CartsService.get_by_user_id_type(
		user_id=token.user_id,
		type=CartType.ACTIVE
	)

	if tmp.error:
		return Mapper.error(tmp.error)

	cart = tmp.result
	tmp = CartsService.get_items_by_cart_id(
		cart_id=cart.id,
		limit=None,
		offset=0
	)
	
	if tmp.error:
		return Mapper.error(tmp.error)
	
	cart_items, _ = tmp.result
	if len(cart_items) == 0:
		return Mapper.router_error('Корзина пуста', 400)

	today = datetime.today()
	track_number = (
		f"TRK{today.year}{today.month:02d}{today.day:02d}-"
		f"{Utils.gen_str(16)}"
	)

	tmp = OrdersService.create(
		track_number=track_number,
		delivery_address=delivery_address,
		created_by=token.user_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)

	order_id, _ = tmp.result
	added_order_item_ids = []
	for cart_item in cart_items:
		tmp = OrdersService.create_item(
			order_id=order_id,
			product_id=cart_item.product_id,
			quantity=cart_item.quantity
		)

		if tmp.error:
			for item_id in added_order_item_ids:
				OrdersService.delete_item(order_item_id=item_id)
			
			OrdersService.set_status(order_id=order_id, status=OrderStatus.CANCELLED, set_by=None)
			return Mapper.error(tmp.error)

		added_order_item_ids.append(tmp.result)

	tmp = CartsService.delete_items_by_cart_id(cart_id=cart.id)
	if tmp.error:
		return Mapper.error(tmp.error)

	return jsonify({
		"success": True,
		"order_id": order_id,
		"track_number": track_number
	}), 201

@client_orders_bp.post('/pay/<int:order_id>')
@require_session
def pay(_, token, order_id: int):
	data = request.get_json()
	amount = Utils.parse_decimal_from_dict(data, 'amount')
	if amount is None:
		return Mapper.router_error('Неверный запрос!', 400)
	
	tmp = OrdersService.get_by_id(order_id=order_id)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	order = tmp.result
	if order.created_by != token.user_id:
		return Mapper.router_error("Это не ваш заказ!", 403)

	tmp = OrderPaymentsService.create(
		order_id=order_id,
		amount=amount,
		payment_method=PaymentMethod.CARD
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	tmp = OrdersService.set_status(
		order_id=order_id,
		status=OrderStatus.CONFIRMED,
		set_by=None
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@client_orders_bp.post('/cancel/<int:order_id>')
@require_session
def cancel(_, token, order_id: int):
	tmp = OrdersService.get_by_id(order_id=order_id)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	order = tmp.result
	if order.created_by != token.user_id:
		return Mapper.router_error("Это не ваш заказ!", 403)

	tmp = OrdersService.set_status(
		order_id=order_id,
		status=OrderStatus.CANCELLED,
		set_by=None
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@client_orders_bp.get('/by-track-number/<string:track_number>')
def by_track_number(track_number: str):
	tmp = OrdersService.get_by_track_number(track_number=track_number)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	order = tmp.result

	tmp = OrdersService.get_total_price(order_id=order.id)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	total_price = tmp.result

	data = request.args.to_dict()
	page = Utils.parse_int_from_dict(data, 'page')
	if page is None or page < 0:
		page = 0

	limit, offset = Utils.page_to_limit_offset(page)
	tmp = OrdersService.get_items_by_order_id(
		order_id=order.id,
		limit=limit,
		offset=offset
	)

	if tmp.error:
		return Mapper.error(tmp.error)

	order = asdict(order)
	
	items, total_items = tmp.result
	order["items"] = [asdict(order_item) for order_item in items]
	return jsonify({
		"success": True,
		'pagination': Utils.build_pagination_dict(offset, limit, page, 'items', total_items),
		"order": order,
		"total_price": total_price
	}), 200

@client_orders_bp.get('/<int:order_id>')
@require_session
def get(_, token, order_id: int):
	tmp = OrdersService.get_by_id(order_id=order_id)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	order = tmp.result
	if order.created_by != token.user_id:
		return Mapper.router_error("Это не ваш заказ!", 403)

	tmp = OrdersService.get_total_price(order_id=order.id)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	total_price = tmp.result

	tmp = OrdersService.get_items_by_order_id(
		order_id=order.id,
		limit=None
	)

	if tmp.error:
		return Mapper.error(tmp.error)

	order = asdict(order)
	
	items, _ = tmp.result
	order["items"] = [asdict(order_item) for order_item in items]
	return jsonify({
		"success": True,
		"order": order,
		"total_price": total_price
	}), 200

@client_orders_bp.get('search')
@require_session
def search(_, token):
	data = request.args.to_dict()
	search_str = Utils.parse_str_from_dict(data, 'search')
	status = Utils.parse_str_enum_from_dict(data, 'status', OrderStatus)
	created_from = Utils.parse_date_from_dict(data, 'created_from')
	created_to = Utils.parse_date_from_dict(data, 'created_to')
	page = Utils.parse_int_from_dict(data, 'page')
	if page is None or page < 0:
		page = 0
	
	limit, offset = Utils.page_to_limit_offset(page)
	tmp = OrdersService.search(
		search=search_str,
		user_id=token.user_id,
		status=status,
		created_from=created_from,
		created_to=created_to,
		limit=limit,
		offset=offset
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	orders, total_orders = tmp.result
	return jsonify({
		"success": True,
		'pagination': Utils.build_pagination_dict(offset, limit, page, 'orders', total_orders),
		"orders": [asdict(order) for order in orders]
	}), 200

@client_orders_bp.get('/total-price/<int:order_id>')
@require_session
def get_total_price(_, token, order_id: int):
	tmp = OrdersService.get_by_id(order_id=order_id)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	order = tmp.result
	if order.created_by != token.user_id:
		return Mapper.router_error('Это не ваш заказ!', 403)

	tmp = OrdersService.get_total_price(order_id=order_id)
	if tmp.error:
		return Mapper.error(tmp.error)

	return jsonify({
		"success": True,
		"total_price": tmp.result
	}), 200
