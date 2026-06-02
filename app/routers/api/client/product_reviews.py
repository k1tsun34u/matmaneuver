from math import ceil
from app.utils import Utils
from dataclasses import asdict
from app.errors.mapper import Mapper
from flask import Blueprint, request, jsonify
from app.session_manager import require_session
from app.services.product_reviews_service import ProductReviewsService
from app.dtos.api.client.response_product_review import ResponseProductReview


client_product_reviews_bp = Blueprint(
	"api_client_product_reviews",
	__name__,
	url_prefix="/api/client/product_reviews"
)

@client_product_reviews_bp.post('/create')
@require_session
def create(_, token):
	data = request.get_json()
	product_id = Utils.parse_int_from_dict(data, 'product_id')
	rating = Utils.parse_int_from_dict(data, 'rating')
	comment = Utils.parse_str_from_dict(data, 'comment')
	if product_id is None or rating is None:
		return Mapper.router_error('Неверный запрос', 400)
	if comment is not None:
		if len(comment.strip()) == 0:
			comment = None
	
	tmp = ProductReviewsService.create(
		product_id=product_id,
		user_id=token.user_id,
		rating=rating,
		comment=comment
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 201

@client_product_reviews_bp.delete('/delete')
@require_session
def delete(_, token):
	data = request.get_json()
	product_id = Utils.parse_int_from_dict(data, 'product_id')
	if product_id is None:
		return Mapper.router_error('Неверный запрос', 400)
	
	tmp = ProductReviewsService.delete(
		product_id=product_id,
		user_id=token.user_id,
		deleted_by=None
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@client_product_reviews_bp.get('/by-product/<int:product_id>')
def by_product(product_id: int):
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
	
	reviews, total_reviews = tmp.result
	return jsonify({
		"success": True,
		'pagination': Utils.build_pagination_dict(offset, limit, page, 'reviews', total_reviews),
		"reviews": [asdict(ResponseProductReview(r)) for r in reviews]
	}), 200

@client_product_reviews_bp.get('/by-user/<int:user_id>')
def by_user(user_id: int):
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
	
	reviews, total_reviews = tmp.result
	return jsonify({
		"success": True,
		'pagination': Utils.build_pagination_dict(offset, limit, page, 'reviews', total_reviews),
		"reviews": [asdict(ResponseProductReview(r)) for r in reviews]
	}), 200

@client_product_reviews_bp.get('/rating/<int:product_id>')
def get_rating(product_id: int):
	tmp = ProductReviewsService.get_average_product_rating(product_id)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"rating": round(float(tmp.result or 0), 2)
	}), 200
