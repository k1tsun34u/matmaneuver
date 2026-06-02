from app.utils import Utils
from dataclasses import asdict
from app.errors.mapper import Mapper
from flask import Blueprint, jsonify, request
from app.session_manager import require_employee_session
from app.services.order_payments_service import OrderPaymentsService
from app.dtos.api.employee.response_order_payment import ResponseOrderPayment


employee_order_payments_bp = Blueprint(
	"api_employee_order_payments",
	__name__,
	url_prefix="/api/employee/order_payments"
)

@employee_order_payments_bp.get('/<int:order_payment_id>')
@require_employee_session
def get(_, __, ___, order_payment_id: int):
	tmp = OrderPaymentsService.get_by_id(order_payment_id=order_payment_id)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"payment": asdict(ResponseOrderPayment(tmp.result))
	}), 200

@employee_order_payments_bp.get('/by-order/<int:order_id>')
@require_employee_session
def by_order(_, __, ___, order_id: int):
	data = request.args.to_dict()
	page = Utils.parse_int_from_dict(data, 'page')
	if page is None or page < 0:
		page = 0

	limit, offset = Utils.page_to_limit_offset(page)
	tmp = OrderPaymentsService.get_many_by_order_id(
		order_id=order_id,
		limit=limit,
		offset=offset
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	order_payments, total_payments = tmp.result
	return jsonify({
		"success": True,
		'pagination': Utils.build_pagination_dict(offset, limit, page, "payments", total_payments),
		"payments": [asdict(ResponseOrderPayment(payment)) for payment in order_payments]
	}), 200

@employee_order_payments_bp.get('/is-fully-paid/<int:order_id>')
@require_employee_session
def is_fully_paid(_, __, ___, order_id: int):
	tmp = OrderPaymentsService.is_fully_paid(order_id=order_id)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"is_fully_paid": tmp.result
	}), 200
