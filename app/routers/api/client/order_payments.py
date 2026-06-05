from app.utils import Utils
from dataclasses import asdict
from app.errors.mapper import Mapper
from flask import Blueprint, jsonify, request
from app.session_manager import require_session
from app.types.payment_method import PaymentMethod
from app.services.orders_service import OrdersService
from app.services.order_payments_service import OrderPaymentsService


client_order_payments_bp = Blueprint(
	"api_client_order_payments",
	__name__,
	url_prefix="/api/client/order_payments"
)

@client_order_payments_bp.post('/create/<int:order_id>')
@require_session
def create(_, token, order_id: int):
	data = request.get_json()
	amount = Utils.parse_decimal_from_dict(data, 'amount')
	payment_method = Utils.parse_str_enum_from_dict(data, 'payment_method', PaymentMethod)
	if amount is None:
		return Mapper.router_error('Неверный запрос!', 400)
	
	# not a big problem
	if payment_method is None:
		payment_method = PaymentMethod.CARD

	tmp = OrdersService.get_by_id(order_id=order_id)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	order = tmp.result
	if order.created_by != token.user_id:
		return Mapper.router_error('Это не ваш заказ!', 403)
	
	tmp = OrderPaymentsService.create(
		order_id=order_id,
		amount=amount,
		payment_method=payment_method
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	return jsonify({"success": True}), 200


@client_order_payments_bp.get('/by-order/<int:order_id>')
@require_session
def by_order(_, token, order_id: int):
	data = request.args.to_dict()
	page = Utils.parse_int_from_dict(data, 'page')
	if page is None or page < 0:
		page = 0
	
	limit, offset = Utils.page_to_limit_offset(page)
	tmp = OrdersService.get_by_id(order_id=order_id)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	order = tmp.result
	if order.created_by != token.user_id:
		return Mapper.router_error('Это не ваш заказ!', 403)

	tmp = OrderPaymentsService.get_many_by_order_id(
		order_id=order_id,
		limit=limit,
		offset=offset
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	payments, total_payments = tmp.result
	return jsonify({
		"success": True,
		'pagination': Utils.build_pagination_dict(offset, limit, page, 'payments', total_payments),
		"payments": [asdict(payment) for payment in payments]
	}), 200

@client_order_payments_bp.get('/my')
@require_session
def my(_, token):
	data = request.args.to_dict()
	page = Utils.parse_int_from_dict(data, 'page')
	if page is None or page < 0:
		page = 0
	
	limit, offset = Utils.page_to_limit_offset(page)
	tmp = OrderPaymentsService.get_many_by_user_id(
		user_id=token.user_id,
		limit=limit,
		offset=offset
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	payments, total_payments = tmp.result
	return jsonify({
		"success": True,
		'pagination': Utils.build_pagination_dict(offset, limit, page, 'payments', total_payments),
		"payments": [asdict(payment) for payment in payments]
	}), 200
