from app.utils import Utils
from dataclasses import asdict
from app.errors.mapper import Mapper
from flask import Blueprint, jsonify, request
from app.session_manager import require_employee_session
from app.services.warehouses_service import WarehousesService
from app.dtos.api.employee.response_warehouse import ResponseWarehouse
from app.dtos.api.employee.response_warehouse_product import ResponseWarehouseProduct
from app.dtos.api.employee.response_complete_warehouse_product import ResponseCompleteWarehouseProduct


employee_warehouses_bp = Blueprint(
	"api_employee_warehouses",
	__name__,
	url_prefix="/api/employee/warehouses"
)

@employee_warehouses_bp.post('/create')
@require_employee_session
def create(_, __, cur_emp_id: int):
	data = request.get_json()
	address = Utils.parse_str_from_dict(data, 'address')
	description = Utils.parse_str_from_dict(data, 'description')
	if address is None:
		return Mapper.router_error('Неверный запрос!')
	
	tmp = WarehousesService.create(
		address=address,
		description=description,
		created_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"warehouse_id": tmp.result
	}), 201
	
@employee_warehouses_bp.post('/set-description/<int:warehouse_id>')
@require_employee_session
def set_description(_, __, cur_emp_id: int, warehouse_id: int):
	data = request.get_json()
	description = Utils.parse_str_from_dict(data, 'description')

	tmp = WarehousesService.set_description(
		warehouse_id=warehouse_id,
		description=description,
		set_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@employee_warehouses_bp.post('/delete/<int:warehouse_id>')
@require_employee_session
def delete(_, __, cur_emp_id: int, warehouse_id: int):
	tmp = WarehousesService.soft_delete(
		warehouse_id=warehouse_id,
		deleted_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@employee_warehouses_bp.post('/restore/<int:warehouse_id>')
@require_employee_session
def restore(_, __, cur_emp_id: int, warehouse_id: int):
	tmp = WarehousesService.restore(
		warehouse_id=warehouse_id,
		restored_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@employee_warehouses_bp.get('/<int:warehouse_id>')
@require_employee_session
def get(_, __, ___, warehouse_id: int):
	tmp = WarehousesService.get_by_id(warehouse_id=warehouse_id)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"warehouse": asdict(ResponseWarehouse(tmp.result))
	}), 200

@employee_warehouses_bp.get('/by-address/<string:address>')
@require_employee_session
def by_address(_, __, ___, address: str):
	tmp = WarehousesService.get_by_address(address=address)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"warehouse": asdict(ResponseWarehouse(tmp.result))
	}), 200

@employee_warehouses_bp.get('/search')
@require_employee_session
def search(_, __, ___):
	data = request.args.to_dict()
	search_str = Utils.parse_str_from_dict(data, 'search')
	page = Utils.parse_int_from_dict(data, 'page')
	exclude_deleted = Utils.parse_bool_from_dict(data, 'exclude_deleted')
	if page is None or page < 0:
		page = 0
	if exclude_deleted is None:
		exclude_deleted = True
	
	limit, offset = Utils.page_to_limit_offset(page)
	tmp = WarehousesService.search(
		search=search_str,
		exclude_deleted=exclude_deleted,
		limit=limit,
		offset=offset
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	warehouses, total_warehouses = tmp.result
	return jsonify({
		"success": True,
		'pagination': Utils.build_pagination_dict(offset, limit, page, "warehouses", total_warehouses),
		"warehouses": [asdict(ResponseWarehouse(warehouse)) for warehouse in warehouses]
	}), 200

@employee_warehouses_bp.post('/add-product/<int:warehouse_id>/<int:product_id>')
@require_employee_session
def add_product(_, __, cur_emp_id: int, warehouse_id: int, product_id: int):
	tmp = WarehousesService.add_product(
		warehouse_id=warehouse_id,
		product_id=product_id,
		added_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"product_id": tmp.result
	}), 200

@employee_warehouses_bp.post('/delete-product/<int:warehouse_id>/<int:product_id>')
@require_employee_session
def delete_product(_, __, cur_emp_id: int, warehouse_id: int, product_id: int):
	tmp = WarehousesService.delete_product(
		warehouse_id=warehouse_id,
		product_id=product_id,
		deleted_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@employee_warehouses_bp.post('/delete-all-products/<int:warehouse_id>')
@require_employee_session
def delete_all_products(_, __, cur_emp_id: int, warehouse_id: int):
	tmp = WarehousesService.delete_all_products(
		warehouse_id=warehouse_id,
		deleted_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@employee_warehouses_bp.post('/increase-product/<int:warehouse_id>/<int:product_id>')
@require_employee_session
def increase_product_quantity(_, __, cur_emp_id: int, warehouse_id: int, product_id: int):
	data = request.get_json()
	quantity = Utils.parse_int_from_dict(data, 'quantity')
	if quantity is None:
		return Mapper.router_error('Неверный запрос!', 400)
	
	tmp = WarehousesService.increase_product_quantity(
		warehouse_id=warehouse_id,
		product_id=product_id,
		quantity=quantity,
		increased_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200
	

@employee_warehouses_bp.post('/decrease-product/<int:warehouse_id>/<int:product_id>')
@require_employee_session
def decrease_product_quantity(_, __, cur_emp_id: int, warehouse_id: int, product_id: int):
	data = request.get_json()
	quantity = Utils.parse_int_from_dict(data, 'quantity')
	if quantity is None:
		return Mapper.router_error('Неверный запрос!', 400)
	
	tmp = WarehousesService.decrease_product_quantity(
		warehouse_id=warehouse_id,
		product_id=product_id,
		quantity=quantity,
		decreased_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@employee_warehouses_bp.post('/reserve-product/<int:warehouse_id>/<int:product_id>')
@require_employee_session
def reserve_product(_, __, ___, warehouse_id: int, product_id: int):
	data = request.get_json()
	quantity = Utils.parse_int_from_dict(data, 'quantity')
	if quantity is None:
		return Mapper.router_error('Неверный запрос!', 400)
	
	tmp = WarehousesService.reserve_product(
		warehouse_id=warehouse_id,
		product_id=product_id,
		reserve_quantity=quantity
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@employee_warehouses_bp.post('/unreserve-product/<int:warehouse_id>/<int:product_id>')
@require_employee_session
def unreserve_product(_, __, ___, warehouse_id: int, product_id: int):
	data = request.get_json()
	quantity = Utils.parse_int_from_dict(data, 'quantity')
	if quantity is None:
		return Mapper.router_error('Неверный запрос!', 400)
	
	tmp = WarehousesService.unreserve_product(
		warehouse_id=warehouse_id,
		product_id=product_id,
		reserve_quantity=quantity
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@employee_warehouses_bp.post('/consume-product/<int:warehouse_id>/<int:product_id>')
@require_employee_session
def consume_product(_, __, ___, warehouse_id: int, product_id: int):
	data = request.get_json()
	quantity = Utils.parse_int_from_dict(data, 'quantity')
	if quantity is None:
		return Mapper.router_error('Неверный запрос!', 400)
	
	tmp = WarehousesService.consume_product(
		warehouse_id=warehouse_id,
		product_id=product_id,
		quantity=quantity
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@employee_warehouses_bp.get('/products/by-warehouse/<int:warehouse_id>')
@require_employee_session
def get_products_by_warehouse(_, __, ___, warehouse_id: int):
	data = request.args.to_dict()
	page = Utils.parse_int_from_dict(data, 'page')
	if page is None or page < 0:
		page = 0
	
	limit, offset = Utils.page_to_limit_offset(page)
	tmp = WarehousesService.get_products_by_warehouse_id(
		warehouse_id=warehouse_id,
		limit=limit,
		offset=offset
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	warehouse_products, total_products = tmp.result
	return jsonify({
		"success": True,
		'pagination': Utils.build_pagination_dict(offset, limit, page, "products", total_products),
		"products": [asdict(ResponseWarehouseProduct(product)) for product in warehouse_products]
	}), 200

@employee_warehouses_bp.get('/products/complete/<int:product_id>')
@require_employee_session
def get_complete_products(_, __, ___, product_id: int):
	data = request.args.to_dict()
	page = Utils.parse_int_from_dict(data, 'page')
	exclude_deleted = Utils.parse_bool_from_dict(data, 'exclude_deleted')
	if page is None or page < 0:
		page = 0
	if exclude_deleted is None:
		exclude_deleted = True
	
	limit, offset = Utils.page_to_limit_offset(page)
	tmp = WarehousesService.get_complete_warehouse_products_by_product_id(
		product_id=product_id,
		exclude_deleted=exclude_deleted,
		limit=limit,
		offset=offset
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	complete_products, total_products = tmp.result
	return jsonify({
		"success": True,
		'pagination': Utils.build_pagination_dict(offset, limit, page, "products", total_products),
		"products": [asdict(ResponseCompleteWarehouseProduct(product)) for product in complete_products]
	}), 200
