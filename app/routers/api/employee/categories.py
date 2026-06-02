from math import ceil
from app.utils import Utils
from dataclasses import asdict
from app.errors.mapper import Mapper
from flask import Blueprint, jsonify, request
from app.session_manager import require_employee_session
from app.services.categories_service import CategoriesService
from app.dtos.api.employee.response_category import ResponseCategory


employee_categories_bp = Blueprint(
	"api_employee_categories",
	__name__,
	url_prefix="/api/employee/categories"
)

@employee_categories_bp.post('/create')
@require_employee_session
def create(_, __, cur_emp_id: int):
	data = request.get_json()
	parent_category_id = Utils.parse_int_from_dict(data, 'parent_category_id')
	name = Utils.parse_str_from_dict(data, 'name')
	if name is None:
		return Mapper.router_error('Неверный запрос!', 400)
	
	tmp = CategoriesService.create(
		parent_category_id=parent_category_id,
		name=name,
		created_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"category_id": tmp.result
	}), 201

@employee_categories_bp.post('/set-parent-category/<int:category_id>')
@require_employee_session
def set_parent_category(_, __, cur_emp_id: int, category_id: int):
	data = request.get_json()
	parent_category_id = Utils.parse_int_from_dict(data, 'parent_category_id')
	
	tmp = CategoriesService.set_parent_category(
		category_id=category_id,
		parent_category_id=parent_category_id,
		set_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@employee_categories_bp.post('/deactivate/<int:category_id>')
@require_employee_session
def deactivate(_, __, cur_emp_id: int, category_id: int):
	tmp = CategoriesService.deactivate(
		category_id=category_id,
		deactivated_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@employee_categories_bp.post('/restore/<int:category_id>')
@require_employee_session
def restore(_, __, cur_emp_id: int, category_id: int):
	tmp = CategoriesService.restore(
		category_id=category_id,
		restored_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@employee_categories_bp.get('/<int:category_id>')
@require_employee_session
def get(_, __, ___, category_id: int):
	tmp = CategoriesService.get_by_id(category_id=category_id)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"category": asdict(ResponseCategory(tmp.result))
	}), 200

@employee_categories_bp.get('/by-name/<string:name>')
@require_employee_session
def by_name(_, __, ___, name: str):
	tmp = CategoriesService.get_by_name(name=name)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"category": asdict(ResponseCategory(tmp.result))
	}), 200

@employee_categories_bp.get('/search')
@require_employee_session
def search(_, __, ___):
	data = request.args.to_dict()
	search_str = Utils.parse_str_from_dict(data, 'search')
	exclude_deactivated = Utils.parse_bool_from_dict(data, 'exclude_deactivated')
	page = Utils.parse_int_from_dict(data, 'page')
	if page is None or page < 0:
		page = 0
	if exclude_deactivated is None:
		exclude_deactivated = True
	
	limit, offset = Utils.page_to_limit_offset(page)
	tmp = CategoriesService.search(
		search=search_str,
		exclude_deactivated=exclude_deactivated,
		limit=limit,
		offset=offset
	)
	
	if tmp.error:
		return Mapper.error(tmp.error)
	
	categories, total_categories = tmp.result
	return jsonify({
		"success": True,
		'pagination': Utils.build_pagination_dict(offset, limit, page, 'categories', total_categories),
		"categories": [asdict(ResponseCategory(category)) for category in categories]
	}), 200
