from app.utils import Utils
from dataclasses import asdict
from app.errors.mapper import Mapper
from flask import Blueprint, jsonify, request
from app.types.supply_status import SupplyStatus
from app.session_manager import require_employee_session
from app.services.supplies_service import SuppliesService
from app.dtos.api.employee.response_supply import ResponseSupply
from app.dtos.api.employee.response_supply_item import ResponseSupplyItem
from app.dtos.api.employee.response_supply_status_history import ResponseSupplyStatusHistory as RSSH


employee_supplies_bp = Blueprint(
	"api_employee_supplies",
	__name__,
	url_prefix="/api/employee/supplies"
)

@employee_supplies_bp.post('/create/<int:supplier_id>')
@require_employee_session
def create(_, __, cur_emp_id: int, supplier_id: int):
	data = request.get_json()
	
	# [
	# 	[
	# 		warehouse_id, planned_delivery_date,
	#		[product_id, quantity], ...
	#	], ...
	# ]
	supplies_data = Utils.parse_list_from_dict(data, 'supplies_data')
	if supplies_data is None or not len(supplies_data):
		return Mapper.router_error('Неверный запрос!', 400)
	
	warehouses = set()
	for item in supplies_data:
		if (
			len(item) < 3 or
			not isinstance(item[0], int) or
			not isinstance(item[1], str) or
			Utils.str_to_date(item[1]) is None
		):
			return Mapper.router_error('Неверный запрос!', 400)
		elif not item[2:]:
			return Mapper.router_error('Для склада не указаны товары!', 400)

		warehouse_id = item[0]
		if warehouse_id in warehouses:
			return Mapper.router_error('Дублирование склада!', 400)
		
		warehouses.add(warehouse_id)

		products_in_supply = set()
		for wh_item in item[2:]:
			if not isinstance(wh_item, list) or any([not isinstance(c, int) for c in wh_item]):
				return Mapper.router_error('Неверный запрос!', 400)
			
			product_id = wh_item[0]
			if product_id in products_in_supply:
				return Mapper.router_error(f'Товар {product_id} дублируется в supply для склада {warehouse_id}!', 400)
			products_in_supply.add(product_id)
	
	supplies = []
	for item in supplies_data:
		warehouse_id = item[0]
		planned_delivery_date = Utils.str_to_date(item[1])
		
		# warning: TODO:
		# no rollback
		tmp = SuppliesService.create(
			supplier_id=supplier_id,
			warehouse_id=warehouse_id,
			planned_delivery_date=planned_delivery_date,
			created_by=cur_emp_id
		)

		if tmp.error:
			return Mapper.error(tmp.error)

		supply_items = []
		supply_id = tmp.result
		for wh_item in item[2:]:
			product_id = wh_item[0]
			quantity = wh_item[1]

			# warning: TODO:
			# no rollback
			tmp = SuppliesService.create_item(
				supply_id=supply_id,
				product_id=product_id,
				quantity=quantity,
				created_by=cur_emp_id
			)

			if tmp.error:
				return Mapper.error(tmp.error)
			
			supply_items.append(tmp.result)
		supplies.append({'id': supply_id, 'items': supply_items})

	return jsonify({
		"success": True,
		"supplies": supplies
	}), 201

@employee_supplies_bp.post('/set-status/<int:supply_id>')
@require_employee_session
def set_status(_, __, cur_emp_id: int, supply_id: int):
	data = request.get_json()
	status = Utils.parse_str_enum_from_dict(data, 'status', SupplyStatus)
	if status is None:
		return Mapper.router_error('Неверный запрос!', 400)
	
	tmp = SuppliesService.set_status(
		supply_id=supply_id,
		status=status,
		set_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@employee_supplies_bp.get('/<int:supply_id>')
@require_employee_session
def get(_, __, ___, supply_id: int):
	tmp = SuppliesService.get_by_id(supply_id=supply_id)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"supply": asdict(tmp.result)
	}), 200

@employee_supplies_bp.get('/by-supplier/<int:supplier_id>')
@require_employee_session
def by_supplier(_, __, ___, supplier_id: int):
	data = request.args.to_dict()
	page = Utils.parse_int_from_dict(data, 'page')
	if page is None or page < 0:
		page = 0
	
	limit, offset = Utils.page_to_limit_offset(page)
	tmp = SuppliesService.get_many_by_supplier_id(
		supplier_id=supplier_id,
		limit=limit,
		offset=offset
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	supplies, total_supplies = tmp.result
	return jsonify({
		"success": True,
		'pagination': Utils.build_pagination_dict(offset, limit, page, "supplies", total_supplies),
		"supplies": [asdict(supply) for supply in supplies]
	}), 200

@employee_supplies_bp.get('/by-warehouse/<int:warehouse_id>')
@require_employee_session
def by_warehouse(_, __, ___, warehouse_id: int):
	data = request.args.to_dict()
	page = Utils.parse_int_from_dict(data, 'page')
	if page is None or page < 0:
		page = 0
	
	limit, offset = Utils.page_to_limit_offset(page)
	tmp = SuppliesService.get_many_by_warehouse_id(
		warehouse_id=warehouse_id,
		limit=limit,
		offset=offset
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	supplies, total_supplies = tmp.result
	return jsonify({
		"success": True,
		'pagination': Utils.build_pagination_dict(offset, limit, page, "supplies", total_supplies),
		"supplies": [asdict(supply) for supply in supplies]
	}), 200

@employee_supplies_bp.get('/search')
@require_employee_session
def search(_, __, ___):
	data = request.args.to_dict()
	status = Utils.parse_str_enum_from_dict(data, 'status', SupplyStatus)
	created_from = Utils.parse_date_from_dict(data, 'created_from')
	created_to = Utils.parse_date_from_dict(data, 'created_to')
	planned_delivery_from = Utils.parse_date_from_dict(data, 'planned_delivery_from')
	planned_delivery_to = Utils.parse_date_from_dict(data, 'planned_delivery_to')
	page = Utils.parse_int_from_dict(data, 'page')
	if page is None or page < 0:
		page = 0
	
	limit, offset = Utils.page_to_limit_offset(page)
	tmp = SuppliesService.search(
		status=status,
		created_from=created_from,
		created_to=created_to,
		planned_delivery_from=planned_delivery_from,
		planned_delivery_to=planned_delivery_to,
		limit=limit,
		offset=offset
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	supplies, total_supplies = tmp.result
	return jsonify({
		"success": True,
		'pagination': Utils.build_pagination_dict(offset, limit, page, "supplies", total_supplies),
		"supplies": [asdict(supply) for supply in supplies]
	}), 200

@employee_supplies_bp.get('/item/<int:supply_item_id>')
@require_employee_session
def get_item(_, __, ___, supply_item_id: int):
	tmp = SuppliesService.get_item_by_id(supply_item_id=supply_item_id)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"item": asdict(tmp.result)
	}), 200

@employee_supplies_bp.get('/items/by-supply/<int:supply_id>')
@require_employee_session
def get_items_by_supply_id(_, __, ___, supply_id: int):
	data = request.args.to_dict()
	page = Utils.parse_int_from_dict(data, 'page')
	if page is None or page < 0:
		page = 0
	
	limit, offset = Utils.page_to_limit_offset(page)
	tmp = SuppliesService.get_items_by_supply_id(
		supply_id=supply_id,
		limit=limit,
		offset=offset
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	supply_items, total_items = tmp.result
	return jsonify({
		"success": True,
		'pagination': Utils.build_pagination_dict(offset, limit, page, "items", total_items),
		"items": [asdict(item) for item in supply_items]
	}), 200

@employee_supplies_bp.get('/items/by-product/<int:product_id>')
@require_employee_session
def get_items_by_product_id(_, __, ___, product_id: int):
	data = request.args.to_dict()
	page = Utils.parse_int_from_dict(data, 'page')
	if page is None or page < 0:
		page = 0
	
	limit, offset = Utils.page_to_limit_offset(page)
	tmp = SuppliesService.get_items_by_product_id(
		product_id=product_id,
		limit=limit,
		offset=offset
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	supply_items, total_items = tmp.result
	return jsonify({
		"success": True,
		'pagination': Utils.build_pagination_dict(offset, limit, page, "items", total_items),
		"items": [asdict(item) for item in supply_items]
	}), 200

@employee_supplies_bp.get('/total-price/<int:supply_id>')
@require_employee_session
def get_total_price(_, __, ___, supply_id: int):
	tmp = SuppliesService.get_total_price(supply_id=supply_id)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"total_price": tmp.result
	}), 200

@employee_supplies_bp.get('/status-history/<int:supply_id>')
@require_employee_session
def get_status_history(_, __, ___, supply_id: int):
	# data = request.args.to_dict()
	# page = Utils.parse_int_from_dict(data, 'page')
	# if page is None or page < 0:
	# 	page = 0

	# warning: TODO:
	# not good, but ok
	page = 0
	limit, offset = Utils.page_to_limit_offset(page)
	tmp = SuppliesService.get_status_history(
		supply_id=supply_id,
		limit=limit,
		offset=offset
	)

	if tmp.error:
		return Mapper.error(tmp.error)

	statuses = tmp.result
	return jsonify({
		"success": True,
		"statuses": [asdict(RSSH(status)) for status in statuses]
	}), 200
