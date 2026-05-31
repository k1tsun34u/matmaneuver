from math import ceil
from app.utils import Utils
from dataclasses import asdict
from app.errors.mapper import Mapper
from flask import Blueprint, request, jsonify
from app.dtos.api.client.response_product import ResponseProduct
from app.dtos.api.client.response_category import ResponseCategory
from app.services.product_categories_service import ProductCategoriesService


client_product_categories_bp = Blueprint(
	"api_client_product_categories",
	__name__,
	url_prefix="/api/client/product_categories"
)

@client_product_categories_bp.get('/by-product/<int:product_id>')
def by_product(product_id: int):
	tmp = ProductCategoriesService.get_categories_by_product_id(product_id)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"categories": [asdict(ResponseCategory(c)) for c in tmp.result]
	}), 200

@client_product_categories_bp.get('/by-category/<int:category_id>')
def by_category(category_id: int):
	data = request.args.to_dict()
	page = Utils.parse_int_from_dict(data, 'page')
	if page is None or page < 0:
		page = 0
	
	limit, offset = Utils.page_to_limit_offset(page)
	tmp = ProductCategoriesService.get_products_by_category_id(
		category_id=category_id,
		limit=limit,
		offset=offset
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	products, total_products = tmp.result
	return jsonify({
		"success": True,
		"pagination": {
			"offset": offset,
			"limit": limit,
			"page": page,
			"total_products":	total_products,
			"total_pages": ceil(total_products / limit) if limit > 0 else 0
		},
		"products": [asdict(ResponseProduct(p)) for p in products]
	}), 200
