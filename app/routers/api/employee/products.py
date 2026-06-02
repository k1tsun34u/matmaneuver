from app.utils import Utils
from dataclasses import asdict
from app.errors.mapper import Mapper
from flask import Blueprint, jsonify, request
from app.session_manager import require_employee_session
from app.services.products_service import ProductsService
from app.dtos.api.employee.response_product import ResponseProduct


employee_products_bp = Blueprint(
	"api_employee_products",
	__name__,
	url_prefix="/api/employee/products"
)

@employee_products_bp.post('/create')
@require_employee_session
def create(_, __, cur_emp_id: int):
	data = request.get_json()
	name = Utils.parse_str_from_dict(data, 'name')
	description = Utils.parse_str_from_dict(data, 'description')
	price = Utils.parse_decimal_from_dict(data, 'price')
	if name is None or price is None:
		return Mapper.router_error('Неверный запрос!', 400)
	
	tmp = ProductsService.create(
		name=name,
		description=description,
		price=price,
		created_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"product_id": tmp.result
	}), 201

@employee_products_bp.post('/set-description/<int:product_id>')
@require_employee_session
def set_description(_, __, cur_emp_id: int, product_id: int):
	data = request.get_json()
	description = Utils.parse_str_from_dict(data, 'description')

	tmp = ProductsService.set_description(
		product_id=product_id,
		description=description,
		set_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@employee_products_bp.post('/set-price/<int:product_id>')
@require_employee_session
def set_price(_, __, cur_emp_id: int, product_id: int):
	data = request.get_json()
	price = Utils.parse_decimal_from_dict(data, 'price')
	if price is None:
		return Mapper.router_error('Неверный запрос!', 400)

	tmp = ProductsService.set_price(
		product_id=product_id,
		price=price,
		set_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@employee_products_bp.post('/delete/<int:product_id>')
@require_employee_session
def delete(_, __, cur_emp_id: int, product_id: int):
	tmp = ProductsService.soft_delete(
		product_id=product_id,
		deleted_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@employee_products_bp.post('/restore/<int:product_id>')
@require_employee_session
def restore(_, __, cur_emp_id: int, product_id: int):
	tmp = ProductsService.restore(
		product_id=product_id,
		restored_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@employee_products_bp.get('/<int:product_id>')
@require_employee_session
def get(_, __, ___, product_id: int):
	tmp = ProductsService.get_by_id(product_id=product_id)
	if tmp.error:
		return Mapper.error(tmp.error)

	return jsonify({
		"success": True,
		"product": asdict(ResponseProduct(tmp.result))
	}), 200

@employee_products_bp.get('/by-employee/<int:employee_id>')
@require_employee_session
def by_employee(_, __, ___, employee_id: int):
	data = request.args.to_dict()
	exclude_deleted = Utils.parse_bool_from_dict(data, 'exclude_deleted')
	page = Utils.parse_int_from_dict(data, 'page')
	if page is None or page < 0:
		page = 0
	if exclude_deleted is None:
		exclude_deleted = True
	
	limit, offset = Utils.page_to_limit_offset(page)
	tmp = ProductsService.get_many_by_employee_id(
		employee_id=employee_id,
		exclude_deleted=exclude_deleted,
		limit=limit,
		offset=offset
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	products, total_products = tmp.result
	return jsonify({
		"success": True,
		'pagination': Utils.build_pagination_dict(offset, limit, page, 'products', total_products),
		"products": [asdict(ResponseProduct(product)) for product in products]
	}), 200

@employee_products_bp.get('/search')
@require_employee_session
def search(_, __, ___):
	data = request.args.to_dict()
	search_str = Utils.parse_str_from_dict(data, 'search')
	min_price = Utils.parse_decimal_from_dict(data, 'min_price')
	max_price = Utils.parse_decimal_from_dict(data, 'max_price')
	exclude_deleted = Utils.parse_bool_from_dict(data, 'exclude_deleted')
	page = Utils.parse_int_from_dict(data, 'page')
	if page is None or page < 0:
		page = 0
	if exclude_deleted is None:
		exclude_deleted = True
	
	limit, offset = Utils.page_to_limit_offset(page)
	tmp = ProductsService.search(
		search=search_str,
		min_price=min_price,
		max_price=max_price,
		exclude_deleted=exclude_deleted,
		limit=limit,
		offset=offset
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	products, total_products = tmp.result
	return jsonify({
		"success": True,
		'pagination': Utils.build_pagination_dict(offset, limit, page, 'products', total_products),
		"products": [asdict(ResponseProduct(product)) for product in products]
	}), 200
