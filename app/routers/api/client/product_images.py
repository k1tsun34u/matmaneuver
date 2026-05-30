from app.config import Config
from app.errors.mapper import Mapper
from flask import Blueprint, jsonify, send_from_directory
from app.services.product_images_service import ProductImagesService


client_product_images_bp = Blueprint(
	"api_client_product_images",
	__name__,
	url_prefix="/api/client/product_images"
)

@client_product_images_bp.get('/<int:image_id>')
def get(image_id: int):
	tmp = ProductImagesService.get_by_id(image_id)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	storage_key = tmp.result.storage_key
	return send_from_directory(Config.PATH_IMAGES, storage_key)

@client_product_images_bp.get('/by-product/<int:product_id>')
def by_product(product_id: int):
	tmp = ProductImagesService.get_many_by_product_id(product_id)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	image_links = []
	for pi in tmp.result:
		image_links.append(f"/api/client/product_images/{pi.id}")
	
	return jsonify({
		"success": True,
		"images": image_links
	}), 200
