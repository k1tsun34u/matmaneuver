from app.utils import Utils
from dataclasses import asdict
from app.errors.mapper import Mapper
from flask import Blueprint, jsonify, request
from app.session_manager import require_employee_session
from app.dtos.api.employee.response_category import ResponseCategory
from app.services.product_categories_service import ProductCategoriesService


employee_product_categories_bp = Blueprint(
	"api_employee_product_categories",
	__name__,
	url_prefix="/api/employee/product_categories"
)

@employee_product_categories_bp.post('/assign-many/<int:product_id>')
@require_employee_session
def assign_many(_, __, cur_emp_id: int, product_id: int):
	data = request.get_json()
	category_ids = Utils.parse_list_from_dict(data, 'category_ids')
	if category_ids is None:
		return Mapper.router_error('Неверный запрос!', 400)
	
	tmp = ProductCategoriesService.assign_many(
		product_id=product_id,
		category_ids=category_ids,
		assigned_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 201

@employee_product_categories_bp.post('/unassign-many/<int:product_id>')
@require_employee_session
def unassign_many(_, __, cur_emp_id: int, product_id: int):
	data = request.get_json()
	category_ids = Utils.parse_list_from_dict(data, 'category_ids')
	if category_ids is None:
		return Mapper.router_error('Неверный запрос!', 400)
	
	tmp = ProductCategoriesService.unassign_many(
		product_id=product_id,
		category_ids=category_ids,
		unassigned_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@employee_product_categories_bp.get('/by-product/<int:product_id>')
@require_employee_session
def by_product(_, __, ___, product_id: int):
	tmp = ProductCategoriesService.get_categories_by_product_id(product_id=product_id)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"categories": [asdict(category) for category in tmp.result]
	}), 200
