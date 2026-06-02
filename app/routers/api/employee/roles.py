from app.utils import Utils
from dataclasses import asdict
from app.errors.mapper import Mapper
from flask import Blueprint, jsonify, request
from app.services.roles_service import RolesService
from app.session_manager import require_employee_session
from app.dtos.api.employee.response_role import ResponseRole


employee_roles_bp = Blueprint(
	"api_employee_roles",
	__name__,
	url_prefix="/api/employee/roles"
)

@employee_roles_bp.post('/create')
@require_employee_session
def create(_, __, cur_emp_id: int):
	data = request.get_json()
	code = Utils.parse_str_from_dict(data, 'code')
	is_system = Utils.parse_bool_from_dict(data, 'is_system')
	if code is None:
		return Mapper.router_error('Неверный запрос!', 400)
	if is_system is None:
		is_system = False
	
	tmp = RolesService.create(
		code=code,
		is_system=is_system,
		created_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"role_id": tmp.result
	}), 201

@employee_roles_bp.post('/deactivate/<int:role_id>')
@require_employee_session
def deactivate(_, __, cur_emp_id: int, role_id: int):
	tmp = RolesService.deactivate(
		role_id=role_id,
		deactivated_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@employee_roles_bp.post('/restore/<int:role_id>')
@require_employee_session
def restore(_, __, cur_emp_id: int, role_id: int):
	tmp = RolesService.restore(
		role_id=role_id,
		restored_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@employee_roles_bp.post('/assign-permissions/<int:role_id>')
@require_employee_session
def assign_permissions(_, __, cur_emp_id: int, role_id: int):
	data = request.get_json()
	permission_ids = Utils.parse_list_from_dict(data, 'permission_ids')
	if permission_ids is None:
		return Mapper.router_error('Неверный запрос!', 400)
	
	tmp = RolesService.assign_permissions(
		role_id=role_id,
		permission_ids=permission_ids,
		assigned_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@employee_roles_bp.post('/unassign-permissions/<int:role_id>')
@require_employee_session
def unassign_permissions(_, __, cur_emp_id: int, role_id: int):
	data = request.get_json()
	permission_ids = Utils.parse_list_from_dict(data, 'permission_ids')
	if permission_ids is None:
		return Mapper.router_error('Неверный запрос!', 400)
	
	tmp = RolesService.unassign_permissions(
		role_id=role_id,
		permission_ids=permission_ids,
		unassigned_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@employee_roles_bp.get('/<int:role_id>')
@require_employee_session
def get(_, __, ___, role_id: int):
	tmp = RolesService.get_by_id(role_id=role_id)
	if tmp.error:
		return Mapper.error(tmp.error)

	return jsonify({
		"success": True,
		"role": asdict(ResponseRole(tmp.result))
	}), 200

@employee_roles_bp.get('/by-code/<string:code>')
@require_employee_session
def by_code(_, __, ___, code: str):
	tmp = RolesService.get_by_code(code=code)
	if tmp.error:
		return Mapper.error(tmp.error)

	return jsonify({
		"success": True,
		"role": asdict(ResponseRole(tmp.result))
	}), 200

@employee_roles_bp.get('/search')
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
	tmp = RolesService.search(
		search=search_str,
		exclude_deactivated=exclude_deactivated,
		limit=limit,
		offset=offset
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	roles, total_roles = tmp.result
	return jsonify({
		"success": True,
		'pagination': Utils.build_pagination_dict(offset, limit, page, 'roles', total_roles),
		"roles": [asdict(ResponseRole(role)) for role in roles]
	}), 200
