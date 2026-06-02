from app.utils import Utils
from dataclasses import asdict
from app.errors.mapper import Mapper
from flask import Blueprint, jsonify, request
from app.session_manager import require_employee_session
from app.services.order_fulfillments_service import OrderFulfillmentsService
from app.dtos.api.employee.response_order_fulfillment import ResponseOrderFulfillment
from app.dtos.api.employee.response_order_fulfillment_item import ResponseOrderFulfillmentItem


employee_order_fulfillments_bp = Blueprint(
	"api_employee_order_fulfillments",
	__name__,
	url_prefix="/api/employee/order_fulfillments"
)

@employee_order_fulfillments_bp.post('/create/<int:order_id>')
@require_employee_session
def create(_, __, cur_emp_id: int, order_id: int):
	data = request.get_json()

	# [
	# 	[warehouse_id, [product_id, quantity], [...], ...],
	# 	[warehouse_id, [...], ...],
	# 	...
	# ]
	fulfillments_data = Utils.parse_list_from_dict(data, 'fulfillments_data')
	if fulfillments_data is None or not len(fulfillments_data):
		return Mapper.router_error('Неверный запрос!', 400)
	
	warehouses = set()
	for item in fulfillments_data:
		if len(item) < 2 or not isinstance(item[0], int):
			return Mapper.router_error('Неверный запрос!', 400)
		elif not item[1:]:
			return Mapper.router_error('Для склада не указаны товары!', 400)
		
		warehouse_id = item[0]
		if warehouse_id in warehouses:
			return Mapper.router_error('Дублирование склада!', 400)
		
		warehouses.add(warehouse_id)

		products_in_fulfillment = set()
		for wh_item in item[1:]:
			if not isinstance(wh_item, list) or any([not isinstance(c, int) for c in wh_item]):
				return Mapper.router_error('Неверный запрос!', 400)
			
			product_id = wh_item[0]
			if product_id in products_in_fulfillment:
				return Mapper.router_error(f'Товар {product_id} дублируется в fulfillment для склада {warehouse_id}!', 400)
			products_in_fulfillment.add(product_id)

	fulfillments = []
	for item in fulfillments_data:
		warehouse_id = item[0]
		
		# warning: TODO:
		# no rollback
		tmp = OrderFulfillmentsService.create(
			order_id=order_id,
			warehouse_id=warehouse_id,
			created_by=cur_emp_id
		)

		if tmp.error:
			return Mapper.error(tmp.error)

		fulfillment_items = []
		order_fulfillment_id = tmp.result
		for wh_item in item[1:]:
			product_id = wh_item[0]
			quantity = wh_item[1]

			# warning: TODO:
			# no rollback
			tmp = OrderFulfillmentsService.create_item(
				order_fulfillment_id=order_fulfillment_id,
				product_id=product_id,
				quantity=quantity,
				created_by=cur_emp_id
			)

			if tmp.error:
				return Mapper.error(tmp.error)
			
			fulfillment_items.append(tmp.result)
		fulfillments.append({'id': order_fulfillment_id, 'items': fulfillment_items})
	
	return jsonify({
		"success": True,
		"fulfillments": fulfillments
	}), 201

@employee_order_fulfillments_bp.get('/<int:order_fulfillment_id>')
@require_employee_session
def get(_, __, ___, order_fulfillment_id: int):
	tmp = OrderFulfillmentsService.get_by_id(order_fulfillment_id=order_fulfillment_id)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"fulfillment": asdict(ResponseOrderFulfillment(tmp.result))
	}), 200
	
@employee_order_fulfillments_bp.get('/by-order/<int:order_id>')
@require_employee_session
def by_order(_, __, ___, order_id: int):
	data = request.args.to_dict()
	page = Utils.parse_int_from_dict(data, 'page')
	if page is None or page < 0:
		page = 0
	
	limit, offset = Utils.page_to_limit_offset(page)
	tmp = OrderFulfillmentsService.get_many_by_order_id(
		order_id=order_id,
		limit=limit,
		offset=offset
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	order_fulfillments, total_fulfillments = tmp.result
	return jsonify({
		"success": True,
		'pagination': Utils.build_pagination_dict(offset, limit, page, "fulfillments", total_fulfillments),
		"fulfillments": [asdict(ResponseOrderFulfillment(fulfillment)) for fulfillment in order_fulfillments]
	}), 200
	
@employee_order_fulfillments_bp.get('/by-warehouse/<int:warehouse_id>')
@require_employee_session
def by_warehouse(_, __, ___, warehouse_id: int):
	data = request.args.to_dict()
	page = Utils.parse_int_from_dict(data, 'page')
	if page is None or page < 0:
		page = 0
	
	limit, offset = Utils.page_to_limit_offset(page)
	tmp = OrderFulfillmentsService.get_many_by_warehouse_id(
		warehouse_id=warehouse_id,
		limit=limit,
		offset=offset
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	order_fulfillments, total_fulfillments = tmp.result
	return jsonify({
		"success": True,
		'pagination': Utils.build_pagination_dict(offset, limit, page, "fulfillments", total_fulfillments),
		"fulfillments": [asdict(ResponseOrderFulfillment(fulfillment)) for fulfillment in order_fulfillments]
	}), 200

@employee_order_fulfillments_bp.get('/item/<int:order_fulfillment_item_id>')
@require_employee_session
def get_item(_, __, ___, order_fulfillment_item_id: int):
	tmp = OrderFulfillmentsService.get_item_by_id(order_fulfillment_item_id=order_fulfillment_item_id)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"item": asdict(ResponseOrderFulfillmentItem(tmp.result))
	}), 200

@employee_order_fulfillments_bp.get('/items/by-order-fulfillment/<int:order_fulfillment_id>')
@require_employee_session
def get_items_by_order_fulfillment(_, __, ___, order_fulfillment_id: int):
	data = request.args.to_dict()
	page = Utils.parse_int_from_dict(data, 'page')
	if page is None or page < 0:
		page = 0
	
	limit, offset = Utils.page_to_limit_offset(page)
	tmp = OrderFulfillmentsService.get_items_by_order_fulfillment_id(
		order_fulfillment_id=order_fulfillment_id,
		limit=limit,
		offset=offset
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	fulfillment_items, total_items = tmp.result
	return jsonify({
		"success": True,
		'pagination': Utils.build_pagination_dict(offset, limit, page, "items", total_items),
		"items": [asdict(ResponseOrderFulfillmentItem(item)) for item in fulfillment_items]
	}), 200

@employee_order_fulfillments_bp.get('/items/by-product/<int:product_id>')
@require_employee_session
def get_items_by_product(_, __, ___, product_id: int):
	data = request.args.to_dict()
	page = Utils.parse_int_from_dict(data, 'page')
	if page is None or page < 0:
		page = 0
	
	limit, offset = Utils.page_to_limit_offset(page)
	tmp = OrderFulfillmentsService.get_items_by_product_id(
		product_id=product_id,
		limit=limit,
		offset=offset
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	fulfillment_items, total_items = tmp.result
	return jsonify({
		"success": True,
		'pagination': Utils.build_pagination_dict(offset, limit, page, "items", total_items),
		"items": [asdict(ResponseOrderFulfillmentItem(item)) for item in fulfillment_items]
	}), 200

@employee_order_fulfillments_bp.get('/fulfilled-quantity/<int:order_id>/<int:product_id>')
@require_employee_session
def get_fulfilled_quantity(_, __, ___, order_id: int, product_id: int):
	tmp = OrderFulfillmentsService.get_total_fulfilled_quantity(
		order_id=order_id,
		product_id=product_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"fulfilled_quantity": tmp.result
	}), 200
