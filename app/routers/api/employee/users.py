from math import ceil
from app.utils import Utils
from dataclasses import asdict
from app.errors.mapper import Mapper
from flask import Blueprint, jsonify, request
from app.services.users_service import UsersService
from app.session_manager import require_employee_session
from app.dtos.api.employee.response_user import ResponseUser


employee_users_bp = Blueprint(
	"api_employee_users",
	__name__,
	url_prefix="/api/employee/users"
)

@employee_users_bp.post('/block/<int:user_id>')
@require_employee_session
def block(_, __, cur_emp_id: int, user_id: int):
	tmp = UsersService.block(
		user_id=user_id,
		blocked_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@employee_users_bp.post('/unblock/<int:user_id>')
@require_employee_session
def unblock(_, __, cur_emp_id: int, user_id: int):
	tmp = UsersService.unblock(
		user_id=user_id,
		unblocked_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@employee_users_bp.post('/delete/<int:user_id>')
@require_employee_session
def delete(_, __, cur_emp_id: int, user_id: int):
	tmp = UsersService.soft_delete(
		user_id=user_id,
		deleted_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@employee_users_bp.post('/restore/<int:user_id>')
@require_employee_session
def restore(_, __, cur_emp_id: int, user_id: int):
	tmp = UsersService.restore(
		user_id=user_id,
		restored_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@employee_users_bp.get('/<int:user_id>')
@require_employee_session
def get(_, __, ___, user_id: int):
	tmp = UsersService.get_by_id(user_id=user_id)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"user": asdict(ResponseUser(tmp.result))
	}), 200

@employee_users_bp.get('/by-phone/<string:phone>')
@require_employee_session
def by_phone(_, __, ___, phone: str):
	tmp = UsersService.get_by_phone(phone=phone)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"user": asdict(ResponseUser(tmp.result))
	}), 200

@employee_users_bp.get('/by-email/<string:email>')
@require_employee_session
def by_email(_, __, ___, email: str):
	tmp = UsersService.get_by_email(email=email)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"user": asdict(ResponseUser(tmp.result))
	}), 200

@employee_users_bp.get('/search')
@require_employee_session
def search(_, __, ___):
	data = request.args.to_dict()
	search_str = Utils.parse_str_from_dict(data, 'search')
	exclude_deleted = Utils.parse_bool_from_dict(data, 'exclude_deleted')
	exclude_blocked = Utils.parse_bool_from_dict(data, 'exclude_blocked')
	page = Utils.parse_int_from_dict(data, 'page')
	if page is None or page < 0:
		page = 0
	if exclude_deleted is None:
		exclude_deleted = True
	if exclude_blocked is None:
		exclude_blocked = True
	
	limit, offset = Utils.page_to_limit_offset(page)
	tmp = UsersService.search(
		search=search_str,
		exclude_deleted=exclude_deleted,
		exclude_blocked=exclude_blocked,
		limit=limit,
		offset=offset
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	users, total_users = tmp.result
	return jsonify({
		"success": True,
		"pagination": {
			"offset": offset,
			"limit": limit,
			"page": page,
			"total_users": total_users,
			"total_pages": ceil(total_users / limit) if limit > 0 else 0
		},
		"users": [asdict(ResponseUser(user)) for user in users]
	}), 200
