from app.utils import Utils
from dataclasses import asdict
from app.errors.mapper import Mapper
from flask import Blueprint, jsonify, request
from app.types.order_status import OrderStatus
from app.services.orders_service import OrdersService
from app.session_manager import require_employee_session
from app.dtos.api.employee.response_order import ResponseOrder
from app.dtos.api.employee.response_order_status_history import ResponseOrderStatusHistory


employee_orders_bp = Blueprint(
	"api_employee_orders",
	__name__,
	url_prefix="/api/employee/orders"
)

@employee_orders_bp.post('/set-status/<int:order_id>')
@require_employee_session
def set_status(_, __, cur_emp_id: int, order_id: int):
	data = request.get_json()
	status = Utils.parse_str_enum_from_dict(data, 'status', OrderStatus)
	if status is None:
		return Mapper.router_error('Неверный запрос!', 400)

	tmp = OrdersService.set_status(
		order_id=order_id,
		status=status,
		set_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@employee_orders_bp.get('/<int:order_id>')
@require_employee_session
def get(_, __, ___, order_id: int):
	tmp = OrdersService.get_by_id(order_id=order_id)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"order": asdict(ResponseOrder(tmp.result))
	}), 200

@employee_orders_bp.get('/by-track-number/<string:track_number>')
@require_employee_session
def by_track_number(_, __, ___, track_number: str):
	tmp = OrdersService.get_by_track_number(track_number=track_number)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"order": asdict(ResponseOrder(tmp.result))
	}), 200

@employee_orders_bp.get('/by-user/<int:user_id>')
@require_employee_session
def by_user(_, __, ___, user_id: int):
	data = request.args.to_dict()
	page = Utils.parse_int_from_dict(data, 'page')
	if page is None or page < 0:
		page = 0
	
	limit, offset = Utils.page_to_limit_offset(page)
	tmp = OrdersService.get_many_by_user_id(
		user_id=user_id,
		limit=limit,
		offset=offset
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	orders, total_orders = tmp.result
	return jsonify({
		"success": True,
		'pagination': Utils.build_pagination_dict(offset, limit, page, 'orders', total_orders),
		"orders": [asdict(ResponseOrder(order)) for order in orders]
	}), 200

@employee_orders_bp.get('/search')
@require_employee_session
def search(_, __, ___):
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
		"orders": [asdict(ResponseOrder(order)) for order in orders]
	}), 200

@employee_orders_bp.get('/total-price/<int:order_id>')
@require_employee_session
def get_total_price(_, __, ___, order_id: int):
	tmp = OrdersService.get_total_price(order_id=order_id)
	if tmp.error:
		return Mapper.error(tmp.error)

	return jsonify({
		"success": True,
		"total_price": tmp.result
	}), 200

@employee_orders_bp.get('/status-history/<int:order_id>')
@require_employee_session
def get_status_history(_, __, ___, order_id: int):
	# data = request.args.to_dict()
	# page = Utils.parse_int_from_dict(data, 'page')
	# if page is None or page < 0:
	# 	page = 0

	# warning: TODO:
	# not good, but ok
	page = 0
	limit, offset = Utils.page_to_limit_offset(page)
	tmp = OrdersService.get_status_history(
		order_id=order_id,
		limit=limit,
		offset=offset
	)

	if tmp.error:
		return Mapper.error(tmp.error)

	statuses = tmp.result
	return jsonify({
		"success": True,
		"statuses": [asdict(ResponseOrderStatusHistory(status)) for status in statuses]
	}), 200
