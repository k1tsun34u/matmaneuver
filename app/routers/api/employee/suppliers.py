from app.utils import Utils
from dataclasses import asdict
from app.errors.mapper import Mapper
from flask import Blueprint, jsonify, request
from app.session_manager import require_employee_session
from app.services.suppliers_service import SuppliersService
from app.dtos.api.employee.response_supplier import ResponseSupplier


employee_suppliers_bp = Blueprint(
	"api_employee_suppliers",
	__name__,
	url_prefix="/api/employee/suppliers"
)

@employee_suppliers_bp.post('/create')
@require_employee_session
def create(_, __, cur_emp_id: int):
	data = request.get_json()
	full_name = Utils.parse_str_from_dict(data, 'full_name')
	phone = Utils.parse_str_from_dict(data, 'phone')
	email = Utils.parse_str_from_dict(data, 'email')
	address = Utils.parse_str_from_dict(data, 'address')
	if full_name is None or phone is None:
		return Mapper.router_error('Неверный запрос!', 400)
	
	tmp = SuppliersService.create(
		full_name=full_name,
		phone=phone,
		email=email,
		address=address,
		created_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"supplier_id": tmp.result
	}), 201
	
@employee_suppliers_bp.post('/update/<int:supplier_id>')
@require_employee_session
def update(_, __, cur_emp_id: int, supplier_id: int):
	data = request.get_json()
	full_name = Utils.parse_str_from_dict(data, 'full_name')
	phone = Utils.parse_str_from_dict(data, 'phone')
	email = Utils.parse_str_from_dict(data, 'email')
	address = Utils.parse_str_from_dict(data, 'address')

	tmp = SuppliersService.update(
		supplier_id=supplier_id,
		full_name=Utils.value_for_update(full_name),
		phone=Utils.value_for_update(phone),
		email=Utils.value_for_update(email),
		address=Utils.value_for_update(address),
		updated_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200
	
@employee_suppliers_bp.post('/deactivate/<int:supplier_id>')
@require_employee_session
def deactivate(_, __, cur_emp_id: int, supplier_id: int):
	tmp = SuppliersService.deactivate(
		supplier_id=supplier_id,
		deactivated_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200
	
@employee_suppliers_bp.post('/restore/<int:supplier_id>')
@require_employee_session
def restore(_, __, cur_emp_id: int, supplier_id: int):
	tmp = SuppliersService.restore(
		supplier_id=supplier_id,
		restored_by=cur_emp_id
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({"success": True}), 200

@employee_suppliers_bp.get('/<int:supplier_id>')
@require_employee_session
def get(_, __, ___, supplier_id: int):
	tmp = SuppliersService.get_by_id(supplier_id=supplier_id)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"supplier": asdict(ResponseSupplier(tmp.result))
	}), 200

@employee_suppliers_bp.get('/by-phone/<string:phone>')
@require_employee_session
def by_phone(_, __, ___, phone: str):
	tmp = SuppliersService.get_by_phone(phone=phone)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"supplier": asdict(ResponseSupplier(tmp.result))
	}), 200

@employee_suppliers_bp.get('/by-email/<string:email>')
@require_employee_session
def by_email(_, __, ___, email: str):
	tmp = SuppliersService.get_by_email(email=email)
	if tmp.error:
		return Mapper.error(tmp.error)
	
	return jsonify({
		"success": True,
		"supplier": asdict(ResponseSupplier(tmp.result))
	}), 200

@employee_suppliers_bp.get('/search')
@require_employee_session
def search(_, __, ___):
	data = request.args.to_dict()
	search_str = Utils.parse_str_from_dict(data, 'search')
	page = Utils.parse_int_from_dict(data, 'page')
	if page is None or page < 0:
		page = 0
	
	limit, offset = Utils.page_to_limit_offset(page)
	tmp = SuppliersService.search(
		search=search_str,
		limit=limit,
		offset=offset
	)

	if tmp.error:
		return Mapper.error(tmp.error)
	
	suppliers, total_suppliers = tmp.result
	return jsonify({
		"success": True,
		'pagination': Utils.build_pagination_dict(offset, limit, page, 'suppliers', total_suppliers),
		"suppliers": [asdict(ResponseSupplier(supplier)) for supplier in suppliers]
	}), 200
