from app.utils import Utils
from dataclasses import asdict
from app.errors.mapper import Mapper
from app.types.cart_type import CartType
from flask import Blueprint, jsonify, request
from app.session_manager import require_session
from app.services.carts_service import CartsService
from app.dtos.api.client.response_cart_item import ResponseCartItem


client_carts_bp = Blueprint(
	"api_client_carts",
	__name__,
	url_prefix="/api/client/carts"
)

def _get_cart(user_id: int, cart_type: CartType):
	tmp = CartsService.get_by_user_id_type(
		user_id=user_id,
		type=cart_type
	)

	if tmp.error:
		return None, Mapper.error(tmp.error)
	return tmp.result, None

def _parse_cart_request():
	data = request.get_json()

	cart_type = Utils.parse_str_enum_from_dict(data, "cart_type", CartType)
	product_id = Utils.parse_int_from_dict(data, "product_id")

	if cart_type is None or product_id is None:
		return None, None, Mapper.router_error('Неверный запрос!', 400)

	return cart_type, product_id, None

@client_carts_bp.post('/add-item')
@require_session
def add(_, token):
	cart_type, product_id, error = _parse_cart_request()
	if error:
		return error
	
	cart, error = _get_cart(token.user_id, cart_type)
	if error:
		return error
	
	tmp = CartsService.add_item_or_increment(
		cart_id=cart.id,
		product_id=product_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@client_carts_bp.post('/dec-item')
@require_session
def dec(_, token):
	cart_type, product_id, error = _parse_cart_request()
	if error:
		return error
	
	cart, error = _get_cart(token.user_id, cart_type)
	if error:
		return error
	
	tmp = CartsService.decrement_item_or_remove(
		cart_id=cart.id,
		product_id=product_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@client_carts_bp.delete('/remove-item')
@require_session
def remove_item(_, token):
	data = request.args.to_dict()
	cart_type = Utils.parse_str_enum_from_dict(data, 'cart_type', CartType)
	product_id = Utils.parse_int_from_dict(data, 'product_id')
	if cart_type is None or product_id is None:
		return Mapper.router_error('Неверный запрос!', 400)
	
	cart, error = _get_cart(token.user_id, cart_type)
	if error:
		return error
	
	tmp = CartsService.remove_item(
		cart_id=cart.id,
		product_id=product_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@client_carts_bp.delete('/remove-items')
@require_session
def remove_items(_, token):
	data = request.args.to_dict()
	cart_type = Utils.parse_str_enum_from_dict(data, 'cart_type', CartType)
	if cart_type is None:
		return Mapper.router_error('Неверный запрос!', 400)
	
	cart, error = _get_cart(token.user_id, cart_type)
	if error:
		return error
	
	tmp = CartsService.delete_items_by_cart_id(cart_id=cart.id)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@client_carts_bp.get('/<string:cart_type>')
@require_session
def get_items(_, token, cart_type: str):
	cart, error = _get_cart(token.user_id, Utils.parse_enum_from_str(cart_type, CartType))
	if error:
		return error
	
	tmp = CartsService.get_items_by_cart_id(cart_id=cart.id)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"items": [asdict(ResponseCartItem(item)) for item in tmp.result]
	}), 200
