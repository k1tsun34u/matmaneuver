from math import ceil
from app.utils import Utils
from dataclasses import asdict
from app.errors.mapper import Mapper
from flask import Blueprint, jsonify, request
from app.session_manager import require_employee_session
from app.services.permissions_service import PermissionsService
from app.dtos.api.employee.response_permission import ResponsePermission


employee_permissions_bp = Blueprint(
	"api_employee_permissions",
	__name__,
	url_prefix="/api/employee/permissions"
)

@employee_permissions_bp.post('/create')
@require_employee_session
def create(_, __, cur_emp_id: int):
	data = request.get_json()
	code = Utils.parse_str_from_dict(data, 'code')
	description = Utils.parse_str_from_dict(data, 'description')
	is_system = Utils.parse_bool_from_dict(data, 'is_system')
	if code is None:
		return Mapper.router_error('Неверный запрос!', 400)
	if is_system is None:
		is_system = False
	
	tmp = PermissionsService.create(
		code=code,
		description=description,
		is_system=is_system,
		created_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"permission_id": tmp.result
	}), 201

@employee_permissions_bp.post('/set-description/<int:permission_id>')
@require_employee_session
def set_description(_, __, cur_emp_id: int, permission_id: int):
	data = request.get_json()
	description = Utils.parse_str_from_dict(data, 'description')

	tmp = PermissionsService.set_description(
		permission_id=permission_id,
		description=description,
		set_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@employee_permissions_bp.post('/deactivate/<int:permission_id>')
@require_employee_session
def deactivate(_, __, cur_emp_id: int, permission_id: int):
	tmp = PermissionsService.deactivate(
		permission_id=permission_id,
		deactivated_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@employee_permissions_bp.post('/restore/<int:permission_id>')
@require_employee_session
def restore(_, __, cur_emp_id: int, permission_id: int):
	tmp = PermissionsService.restore(
		permission_id=permission_id,
		restored_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@employee_permissions_bp.get('/<int:permission_id>')
@require_employee_session
def get(_, __, ___, permission_id: int):
	tmp = PermissionsService.get_by_id(permission_id=permission_id)
	if tmp.error:
		return Mapper.error(tmp.error)

	return jsonify({
		"success": True,
		"permission": asdict(ResponsePermission(tmp.result))
	}), 200

@employee_permissions_bp.get('/by-code/<string:code>')
@require_employee_session
def by_code(_, __, ___, code: str):
	tmp = PermissionsService.get_by_code(code=code)
	if tmp.error:
		return Mapper.error(tmp.error)

	return jsonify({
		"success": True,
		"permission": asdict(ResponsePermission(tmp.result))
	}), 200

@employee_permissions_bp.get('/search')
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
	tmp = PermissionsService.search(
		search=search_str,
		exclude_deactivated=exclude_deactivated,
		limit=limit,
		offset=offset
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	permissions, total_permissions = tmp.result
	return jsonify({
		"success": True,
		"pagination": {
			"offset": offset,
			"limit": limit,
			"page": page,
			"total_permissions": total_permissions,
			"total_pages": ceil(total_permissions / limit) if limit > 0 else 0
		},
		"permissions": [asdict(ResponsePermission(permission)) for permission in permissions]
	}), 200
