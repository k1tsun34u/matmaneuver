from math import ceil
from app.utils import Utils
from dataclasses import asdict
from app.errors.mapper import Mapper
from flask import Blueprint, jsonify, request
from app.services.users_service import UsersService
from app.session_manager import require_employee_session
from app.services.employees_service import EmployeesService
from app.dtos.api.employee.response_role import ResponseRole
from app.dtos.api.employee.response_employee import ResponseEmployee
from app.dtos.api.employee.response_permission import ResponsePermission
from app.dtos.api.employee.response_employee_user import ResponseEmployeeUser


employee_employees_bp = Blueprint(
	"api_employee_employees",
	__name__,
	url_prefix="/api/employee/employees"
)

@employee_employees_bp.post('/register')
@require_employee_session
def register(_, __, cur_emp_id: int):
	data = request.get_json()
	user_id = Utils.parse_int_from_dict(data, 'user_id')
	# hired_by = Utils.parse_int_from_dict(data, 'hired_by')
	hired_at = Utils.parse_date_from_dict(data, 'hired_at')
	# if user_id is None or hired_by is None or hired_at is None:
	if user_id is None or hired_at is None:
		return Mapper.router_error('Неверный запрос!', 400)
	
	tmp = UsersService.get_by_id(user_id=user_id)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	user = tmp.result
	tmp = EmployeesService.register(
		user_id=user_id,
		hired_by=cur_emp_id,
		hired_at=hired_at,
		created_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	# return jsonify({
	# 	"success": True,
	# 	"session": SessionManager.compose_token(user.id, user.token_ver)
	# }), 201

	return jsonify({"success": True}), 201

# login as client: api/client/auth.py

@employee_employees_bp.post('/fire/<int:tgt_emp_id>')
@require_employee_session
def fire(_, __, cur_emp_id: int, tgt_emp_id: int):
	tmp = EmployeesService.fire(
		employee_id=tgt_emp_id,
		fired_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@employee_employees_bp.post('/rehire/<int:tgt_emp_id>')
@require_employee_session
def rehire(_, __, cur_emp_id: int, tgt_emp_id: int):
	tmp = EmployeesService.rehire(
		employee_id=tgt_emp_id,
		hired_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@employee_employees_bp.post('/assign-roles/<int:tgt_emp_id>')
@require_employee_session
def assign_roles(_, __, cur_emp_id: int, tgt_emp_id: int):
	data = request.get_json()
	role_ids = Utils.parse_list_from_dict(data, 'role_ids')
	if role_ids is None:
		return Mapper.router_error('Неверный запрос!', 400)
	
	tmp = EmployeesService.assign_roles(
		employee_id=tgt_emp_id,
		role_ids=role_ids,
		assigned_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@employee_employees_bp.post('/unassign-roles/<int:tgt_emp_id>')
@require_employee_session
def unassign_roles(_, __, cur_emp_id: int, tgt_emp_id: int):
	data = request.get_json()
	role_ids = Utils.parse_list_from_dict(data, 'role_ids')
	if role_ids is None:
		return Mapper.router_error('Неверный запрос!', 400)
	
	tmp = EmployeesService.unassign_roles(
		employee_id=tgt_emp_id,
		role_ids=role_ids,
		unassigned_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@employee_employees_bp.get('/<int:tgt_emp_id>')
@require_employee_session
def get(_, __, ___, tgt_emp_id: int):
	tmp = EmployeesService.get_by_id(tgt_emp_id)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"employee": asdict(ResponseEmployee(tmp.result))
	}), 200

@employee_employees_bp.get('/by-user/<int:user_id>')
@require_employee_session
def by_user(_, __, ___, user_id: int):
	tmp = EmployeesService.get_by_user_id(user_id=user_id)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"employee": asdict(ResponseEmployee(tmp.result))
	}), 200

@employee_employees_bp.get('/search')
@require_employee_session
def search(_, __, ___):
	data = request.args.to_dict()
	search_str = Utils.parse_str_from_dict(data, 'search')
	exclude_fired = Utils.parse_bool_from_dict(data, 'exclude_fired')
	page = Utils.parse_int_from_dict(data, 'page')
	if page is None or page < 0:
		page = 0
	if exclude_fired is None:
		exclude_fired = True
	
	limit, offset = Utils.page_to_limit_offset(page)
	tmp = EmployeesService.search(
		search=search_str,
		exclude_fired=exclude_fired,
		limit=limit,
		offset=offset
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	employee_users, total_employees = tmp.result
	return jsonify({
		"success": True,
		"pagination": {
			"offset": offset,
			"limit": limit,
			"page": page,
			"total_employees": total_employees,
			"total_pages": ceil(total_employees / limit) if limit > 0 else 0
		},
		"employee_users": [asdict(employee_user) for employee_user in employee_users]
	}), 200

@employee_employees_bp.get('/roles/<int:tgt_emp_id>')
@require_employee_session
def get_roles(_, __, ___, tgt_emp_id: int):
	tmp = EmployeesService.get_roles(employee_id=tgt_emp_id)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"roles": [asdict(ResponseRole(role)) for role in tmp.result]
	}), 200

@employee_employees_bp.get('/permissions/<int:tgt_emp_id>')
@require_employee_session
def get_permissions(_, __, ___, tgt_emp_id: int):
	tmp = EmployeesService.get_permissions(employee_id=tgt_emp_id)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"permissions": [asdict(ResponsePermission(permission)) for permission in tmp.result]
	}), 200

@employee_employees_bp.get('/me')
@require_employee_session
def me(user, _, cur_emp_id: int):
	tmp = EmployeesService.get_by_id(employee_id=cur_emp_id)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	emp = tmp.result
	emp_user = ResponseEmployeeUser(
		id=cur_emp_id,
		user_id=user.id,
		hired_by=emp.hired_by,
		hired_at=emp.hired_at,
		fired_by=emp.fired_by,
		fired_at=emp.fired_at,
		created_by=emp.created_by,
		created_at=emp.created_at,
		phone=user.phone,
		email=user.email,
		full_name=user.full_name
	)

	return jsonify({
		"success": True,
		"employee_user": asdict(emp_user)
	}), 200
