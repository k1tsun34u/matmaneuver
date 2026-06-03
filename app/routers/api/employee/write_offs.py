from app.utils import Utils
from dataclasses import asdict
from app.errors.mapper import Mapper
from flask import Blueprint, jsonify, request
from app.types.write_off_reason import WriteOffReason
from app.session_manager import require_employee_session
from app.services.write_offs_service import WriteOffsService
from app.dtos.api.employee.response_write_off import ResponseWriteOff
from app.dtos.api.employee.response_write_off_item import ResponseWriteOffItem


employee_write_offs_bp = Blueprint(
	"api_employee_write_offs",
	__name__,
	url_prefix="/api/employee/write_offs"
)

@employee_write_offs_bp.post('/create/<int:warehouse_id>')
@require_employee_session
def create(_, __, cur_emp_id: int, warehouse_id: int):
	data = request.get_json()
	reason = Utils.parse_str_enum_from_dict(data, 'reason', WriteOffReason)
	comment = Utils.parse_str_from_dict(data, 'comment')

	# [[product_id, quantity], ...]
	write_offs_data = Utils.parse_list_from_dict(data, 'write_offs_data')
	if (
		reason is None or
		write_offs_data is None or
		len(write_offs_data) < 1
	):
		return Mapper.router_error('Неверный запрос!', 400)
	
	products = set()
	for item in write_offs_data:
		if (
			len(item) != 2 or 
			any ([not isinstance(c, int) for c in item])
		):
			return Mapper.router_error('Неверный запрос!', 400)
		
		product_id = item[0]
		if product_id in products:
			return Mapper.router_error('Дублирование товара!', 400)
		
		products.add(product_id)

	tmp = WriteOffsService.create(
		warehouse_id=warehouse_id,
		reason=reason,
		comment=comment,
		created_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	write_off_items = []
	write_off_id = tmp.result
	for item in write_offs_data:
		product_id = item[0]
		quantity = item[1]

		# warning: TODO:
		# no rollback
		tmp = WriteOffsService.create_item(
			write_off_id=write_off_id,
			product_id=product_id,
			quantity=quantity,
			created_by=cur_emp_id
		)

		if tmp.error:
			return Mapper.error(tmp.error)
		
		write_off_items.append(tmp.result)
	
	return jsonify({
		"success": True,
		"write_off": {'id': write_off_id, 'items': write_off_items}
	}), 201

@employee_write_offs_bp.get('/<int:write_off_id>')
@require_employee_session
def get(_, __, ___, write_off_id: int):
	tmp = WriteOffsService.get_by_id(write_off_id=write_off_id)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"write_off": asdict(ResponseWriteOff(tmp.result))
	}), 200

@employee_write_offs_bp.get('/by-warehouse/<int:warehouse_id>')
@require_employee_session
def by_warehouse(_, __, ___, warehouse_id: int):
	data = request.args.to_dict()
	page = Utils.parse_int_from_dict(data, 'page')
	if page is None or page < 0:
		page = 0
	
	limit, offset = Utils.page_to_limit_offset(page)
	tmp = WriteOffsService.get_many_by_warehouse_id(
		warehouse_id=warehouse_id,
		limit=limit,
		offset=offset
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	write_offs, total_write_offs = tmp.result
	return jsonify({
		"success": True,
		'pagination': Utils.build_pagination_dict(offset, limit, page, "write_offs", total_write_offs),
		"write_offs": [asdict(ResponseWriteOff(write_off)) for write_off in write_offs]
	}), 200

@employee_write_offs_bp.get('/search')
@require_employee_session
def search(_, __, ___):
	data = request.args.to_dict()
	search_str = Utils.parse_str_from_dict(data, 'search')
	warehouse_id = Utils.parse_int_from_dict(data, 'warehouse_id')
	reason = Utils.parse_str_enum_from_dict(data, 'reason', WriteOffReason)
	created_from = Utils.parse_date_from_dict(data, 'created_from')
	created_to = Utils.parse_date_from_dict(data, 'created_to')
	page = Utils.parse_int_from_dict(data, 'page')
	if page is None or page < 0:
		page = 0
	
	limit, offset = Utils.page_to_limit_offset(page)
	tmp = WriteOffsService.search(
		search=search_str,
		warehouse_id=warehouse_id,
		reason=reason,
		created_from=created_from,
		created_to=created_to,
		limit=limit,
		offset=offset
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	write_offs, total_write_offs = tmp.result
	return jsonify({
		"success": True,
		'pagination': Utils.build_pagination_dict(offset, limit, page, "write_offs", total_write_offs),
		"write_offs": [asdict(ResponseWriteOff(write_off)) for write_off in write_offs]
	}), 200

@employee_write_offs_bp.get('/item/<int:write_off_item_id>')
@require_employee_session
def get_item(_, __, ___, write_off_item_id: int):
	tmp = WriteOffsService.get_item_by_id(write_off_item_id=write_off_item_id)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"item": asdict(ResponseWriteOffItem(tmp.result))
	}), 200

@employee_write_offs_bp.get('/items/by-write-off/<int:write_off_id>')
@require_employee_session
def get_items_by_write_off(_, __, ___, write_off_id: int):
	data = request.args.to_dict()
	page = Utils.parse_int_from_dict(data, 'page')
	if page is None or page < 0:
		page = 0
	
	limit, offset = Utils.page_to_limit_offset(page)
	tmp = WriteOffsService.get_items_by_write_off_id(
		write_off_id=write_off_id,
		limit=limit,
		offset=offset
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	write_off_items, total_items = tmp.result
	return jsonify({
		"success": True,
		'pagination': Utils.build_pagination_dict(offset, limit, page, "items", total_items),
		"items": [asdict(ResponseWriteOffItem(item)) for item in write_off_items]
	}), 200

@employee_write_offs_bp.get('/items/by-product/<int:product_id>')
@require_employee_session
def get_items_by_product(_, __, ___, product_id: int):
	data = request.args.to_dict()
	page = Utils.parse_int_from_dict(data, 'page')
	if page is None or page < 0:
		page = 0
	
	limit, offset = Utils.page_to_limit_offset(page)
	tmp = WriteOffsService.get_items_by_product_id(
		product_id=product_id,
		limit=limit,
		offset=offset
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	write_off_items, total_items = tmp.result
	return jsonify({
		"success": True,
		'pagination': Utils.build_pagination_dict(offset, limit, page, "items", total_items),
		"items": [asdict(ResponseWriteOffItem(item)) for item in write_off_items]
	}), 200
