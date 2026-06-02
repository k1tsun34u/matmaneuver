from math import ceil
from app.utils import Utils
from dataclasses import asdict
from app.errors.mapper import Mapper
from flask import Blueprint, request, jsonify
from app.services.products_service import ProductsService
from app.dtos.api.client.response_product import ResponseProduct


client_products_bp = Blueprint(
	"api_client_products",
	__name__,
	url_prefix="/api/client/products"
)

@client_products_bp.get('/<int:product_id>')
def get(product_id: int):
	tmp = ProductsService.get_by_id(product_id)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"product": asdict(ResponseProduct(tmp.result))
	}), 200

@client_products_bp.get('/')
def search():
	data = request.args.to_dict()
	search = Utils.parse_str_from_dict(data, 'search')
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
		search=search,
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
		"products": [asdict(ResponseProduct(p)) for p in products]
	}), 200
