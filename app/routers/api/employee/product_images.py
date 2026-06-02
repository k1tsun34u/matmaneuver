import os
import uuid
from app.utils import Utils
from app.config import Config
from dataclasses import asdict
from app.errors.mapper import Mapper
from flask import Blueprint, jsonify, request
from app.session_manager import require_employee_session
from app.services.product_images_service import ProductImagesService
from app.dtos.api.employee.response_product_image import ResponseProductImage


employee_product_images_bp = Blueprint(
	"api_employee_product_images",
	__name__,
	url_prefix="/api/employee/product_images"
)

@employee_product_images_bp.post('/create-many/<int:product_id>')
@require_employee_session
def create_many(_, __, cur_emp_id: int, product_id: int):
	file_keys = sorted(
		[key for key in request.files if key.startswith('img-')],
		key=lambda x: int(x.split('-')[1])
	)

	if not file_keys:
		return Mapper.router_error('Неверный запрос!', 400)
	
	imgs = []
	index = 0
	last_error = None
	for key in file_keys:
		file = request.files[key]
		if not file:
			return Mapper.router_error('Не удалось получить изображение!', 400)
		
		filename = file.filename or ''
		dot = filename.rfind('.')
		if filename == '':
			return Mapper.router_error('Изображение не выбрано!', 400)
		elif dot == -1:
			return Mapper.router_error('Неизвестный тип изображения!', 415)
		
		ext = filename[dot + 1:]
		if ext.lower() not in ('jpg', 'jpeg', 'png', 'webp', 'svg', 'gif',):
			return Mapper.router_error('Неизвестный тип изображения!', 415)

		storage_key = f"{product_id}-{index}-{uuid.uuid4().hex}.{ext}"
		path_to_img = os.path.join(Config.PATH_IMAGES, storage_key)
		file.save(path_to_img)

		tmp = ProductImagesService.create(
			product_id=product_id,
			storage_key=storage_key,
			created_by=cur_emp_id
		)

		if tmp.error:
			last_error = Mapper.error(tmp.error)
			os.remove(path_to_img)
			continue

		imgs.append({
			"image_id": tmp.result,
			"storage_key": storage_key
		})

		index += 1
	
	if last_error is not None:
		return last_error
	
	return jsonify({
		"success": True,
		"images": imgs
	}), 201

@employee_product_images_bp.post('/delete/<int:product_image_id>')
@require_employee_session
def delete(_, __, cur_emp_id: int, product_image_id: int):
	tmp = ProductImagesService.delete(
		product_image_id=product_image_id,
		deleted_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@employee_product_images_bp.post('/delete-all/<int:product_id>')
@require_employee_session
def delete_all(_, __, cur_emp_id: int, product_id: int):
	tmp = ProductImagesService.delete_many_by_product_id(
		product_id=product_id,
		deleted_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@employee_product_images_bp.get('/<int:product_image_id>')
@require_employee_session
def get(_, __, ___, product_image_id: int):
	tmp = ProductImagesService.get_by_id(product_image_id=product_image_id)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"image": asdict(ResponseProductImage(tmp.result))
	}), 200

@employee_product_images_bp.get('/by-storage-key/<string:storage_key>')
@require_employee_session
def by_storage_key(_, __, ___, storage_key: str):
	tmp = ProductImagesService.get_by_storage_key(storage_key=storage_key)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"image": asdict(ResponseProductImage(tmp.result))
	}), 200

@employee_product_images_bp.get('/by-product/<int:product_id>')
@require_employee_session
def by_product(_, __, ___, product_id: int):
	tmp = ProductImagesService.get_many_by_product_id(product_id=product_id)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"images": [asdict(ResponseProductImage(product_image)) for product_image in tmp.result]
	}), 200

@employee_product_images_bp.get('/by-employee/<int:employee_id>')
@require_employee_session
def by_employee(_, __, ___, employee_id: int):
	data = request.args.to_dict()
	page = Utils.parse_int_from_dict(data, 'page')
	if page is None or page < 0:
		page = 0
	
	limit, offset = Utils.page_to_limit_offset(page)
	tmp = ProductImagesService.get_many_by_employee_id(
		employee_id=employee_id,
		limit=limit,
		offset=offset
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	product_images, total_images = tmp.result
	return jsonify({
		"success": True,
		'pagination': Utils.build_pagination_dict(offset, limit, page, 'images', total_images),
		"images": [asdict(ResponseProductImage(product_image)) for product_image in product_images]
	}), 200
