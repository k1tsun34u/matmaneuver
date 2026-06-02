from app.utils import Utils
from dataclasses import asdict
from app.errors.mapper import Mapper
from flask import Blueprint, jsonify, request
from app.session_manager import require_employee_session
from app.services.product_reviews_service import ProductReviewsService
from app.dtos.api.employee.response_product_review import ResponseProductReview


employee_product_reviews_bp = Blueprint(
	"api_employee_product_reviews",
	__name__,
	url_prefix="/api/employee/product_reviews"
)

@employee_product_reviews_bp.post('/delete/<int:product_id>/<int:user_id>')
@require_employee_session
def delete(_, __, cur_emp_id: int, product_id: int, user_id: int):
	tmp = ProductReviewsService.delete(
		product_id=product_id,
		user_id=user_id,
		deleted_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@employee_product_reviews_bp.post('/by-product/<int:product_id>/delete-all')
@require_employee_session
def delete_all_by_product(_, __, cur_emp_id: int, product_id: int):
	tmp = ProductReviewsService.delete_many_by_product_id(
		product_id=product_id,
		deleted_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@employee_product_reviews_bp.post('/by-user/<int:user_id>/delete-all')
@require_employee_session
def delete_all_by_user(_, __, cur_emp_id: int, user_id: int):
	tmp = ProductReviewsService.delete_many_by_user_id(
		user_id=user_id,
		deleted_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@employee_product_reviews_bp.get('/by-product/<int:product_id>')
@require_employee_session
def by_product(_, __, ___, product_id: int):
	data = request.args.to_dict()
	page = Utils.parse_int_from_dict(data, 'page')
	if page is None or page < 0:
		page = 0
	
	limit, offset = Utils.page_to_limit_offset(page)
	tmp = ProductReviewsService.get_many_by_product_id(
		product_id=product_id,
		limit=limit,
		offset=offset
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	product_reviews, total_reviews = tmp.result
	return jsonify({
		"success": True,
		'pagination': Utils.build_pagination_dict(offset, limit, page, 'reviews', total_reviews),
		"reviews": [asdict(ResponseProductReview(product_review)) for product_review in product_reviews]
	}), 200

@employee_product_reviews_bp.get('/by-user/<int:user_id>')
@require_employee_session
def by_user(_, __, ___, user_id: int):
	data = request.args.to_dict()
	page = Utils.parse_int_from_dict(data, 'page')
	if page is None or page < 0:
		page = 0
	
	limit, offset = Utils.page_to_limit_offset(page)
	tmp = ProductReviewsService.get_many_by_user_id(
		user_id=user_id,
		limit=limit,
		offset=offset
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	product_reviews, total_reviews = tmp.result
	return jsonify({
		"success": True,
		'pagination': Utils.build_pagination_dict(offset, limit, page, 'reviews', total_reviews),
		"reviews": [asdict(ResponseProductReview(product_review)) for product_review in product_reviews]
	}), 200

@employee_product_reviews_bp.get('/rating/<int:product_id>')
@require_employee_session
def get_rating(_, __, ___, product_id: int):
	tmp = ProductReviewsService.get_average_product_rating(product_id=product_id)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"rating": round(float(tmp.result or 0), 2)
	}), 200
