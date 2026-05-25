import psycopg
from app.utils import Utils
from app.unset import Unset, UNSET
from app.models.public.supplier import Supplier
from app.types.update_result import UpdateResult
from app.services.base_service import BaseService
from app.types.service_result import ServiceResult
from app.errors.not_found_error import NotFoundError
from app.types.permission_code import PermissionCode
from app.errors.not_allowed_error import NotAllowedError
from app.types.transaction_helper import TransactionHelper
from app.errors.invalid_value_error import InvalidValueError
from app.repositories.public.suppliers_repository import SuppliersRepository
from app.repositories.public.employee_permissions_repository import EmployeePermissionsRepository as EPR


class SuppliersService(BaseService):
	KEY_HELPERS = (TransactionHelper(Supplier.ENTITY, Supplier.TABLE, (
		Supplier.COLUMN_PHONE,
		Supplier.COLUMN_EMAIL,
	)),)

	FKEY_HELPERS = (TransactionHelper(Supplier.ENTITY, Supplier.TABLE, (
		Supplier.COLUMN_DEACTIVATED_BY,
		Supplier.COLUMN_CREATED_BY,
	)),)

	@classmethod
	def _normalize_fields_or_catch(
		cls,
		full_name: str | Unset,
		phone: str | Unset,
		email: str | None | Unset,
	) -> tuple[str | Unset, str | Unset, str | None | Unset] | InvalidValueError:
		if not isinstance(full_name, Unset):
			normalized_full_name = Utils.normalize_full_name(full_name)
			if not Utils.is_valid_full_name(normalized_full_name):
				return InvalidValueError(Supplier.ENTITY, Supplier.COLUMN_FULL_NAME)

			full_name = normalized_full_name
		
		if not isinstance(phone, Unset):
			normalized_phone = Utils.normalize_phone(phone)
			if not Utils.is_valid_phone(normalized_phone):
				return InvalidValueError(Supplier.ENTITY, Supplier.COLUMN_PHONE)
			
			phone = normalized_phone
		
		if not (isinstance(email, Unset) or email is None):
			normalized_email = Utils.normalize_email(email)
			if not Utils.is_valid_email(normalized_email):
				return InvalidValueError(Supplier.ENTITY, Supplier.COLUMN_EMAIL)
			
			email = normalized_email
		
		return (
			full_name,
			phone,
			email,
		)

	@classmethod
	@BaseService.transaction
	def create(
		cls,
		cur: psycopg.Cursor,
		full_name: str,
		phone: str,
		email: str | None,
		address: str | None,
		created_by: int | None
	) -> ServiceResult:
		"""
			Errors:
			- InvalidValueError
			- NotAllowedError
			- AlreadyExistsError
			- NotFoundError
			- UnhandledError
		"""

		normalized = cls._normalize_fields_or_catch(full_name, phone, email)
		if isinstance(normalized, InvalidValueError):
			return ServiceResult(error=normalized)
		
		norm_full_name, norm_phone, norm_email = normalized
		if created_by is not None and not EPR.has_permission(cur, created_by, PermissionCode.CREATE_SUPPLIER):
			return ServiceResult(error=NotAllowedError(PermissionCode.CREATE_SUPPLIER, Supplier.COLUMN_CREATED_BY))
		
		return ServiceResult(
			result=SuppliersRepository.create(
				cur=cur,
				full_name=norm_full_name,
				phone=norm_phone,
				email=norm_email,
				address=address,
				created_by=created_by
			)
		)
	
	@classmethod
	@BaseService.transaction
	def update(
		cls,
		cur: psycopg.Cursor,
		supplier_id: int,
		full_name: str | Unset = UNSET,
		phone: str | Unset = UNSET,
		email: str | None | Unset = UNSET,
		address: str | None | Unset = UNSET,
		updated_by: int | None = None
	) -> ServiceResult:
		"""
			Errors:
			- InvalidValueError
			- NotAllowedError
			- AlreadyExistsError
			- NotFoundError
			- UnhandledError
		"""

		normalized = cls._normalize_fields_or_catch(full_name, phone, email)
		if isinstance(normalized, InvalidValueError):
			return ServiceResult(error=normalized)
		
		norm_full_name, norm_phone, norm_email = normalized
		if updated_by is not None and not EPR.has_permission(cur, updated_by, PermissionCode.SET_SUPPLIER_FIELDS):
			return ServiceResult(error=NotAllowedError(PermissionCode.SET_SUPPLIER_FIELDS))
		
		updated = SuppliersRepository.update(
			cur=cur,
			supplier_id=supplier_id,
			full_name=norm_full_name,
			phone=norm_phone,
			email=norm_email,
			address=address
		)
		
		if updated == UpdateResult.FAIL_NOT_FOUND:
			return ServiceResult(error=NotFoundError(Supplier.ENTITY, Supplier.COLUMN_ID))
		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def deactivate(
		cls,
		cur: psycopg.Cursor,
		supplier_id: int,
		deactivated_by: int | None
	) -> ServiceResult:
		"""
			Errors:
			- NotAllowedError
			- NotFoundError
			- UnhandledError
		"""
		
		if deactivated_by is not None and not EPR.has_permission(cur, deactivated_by, PermissionCode.DEACTIVATE_SUPPLIER):
			return ServiceResult(error=NotAllowedError(PermissionCode.DEACTIVATE_SUPPLIER, Supplier.COLUMN_DEACTIVATED_BY))

		if SuppliersRepository.deactivate(cur, supplier_id, deactivated_by) == UpdateResult.FAIL_NOT_FOUND:
			return ServiceResult(error=NotFoundError(Supplier.ENTITY, Supplier.COLUMN_ID))
		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def restore(
		cls,
		cur: psycopg.Cursor,
		supplier_id: int,
		restored_by: int | None
	) -> ServiceResult:
		"""
			Errors:
			- NotAllowedError
			- NotFoundError
			- UnhandledError
		"""
		
		if restored_by is not None and not EPR.has_permission(cur, restored_by, PermissionCode.CREATE_SUPPLIER):
			return ServiceResult(error=NotAllowedError(PermissionCode.CREATE_SUPPLIER))

		if SuppliersRepository.restore(cur, supplier_id) == UpdateResult.FAIL_NOT_FOUND:
			return ServiceResult(error=NotFoundError(Supplier.ENTITY, Supplier.COLUMN_ID))
		return ServiceResult()
	
	@classmethod
	@BaseService.transaction
	def get_by_id(
		cls,
		cur: psycopg.Cursor,
		supplier_id: int
	) -> ServiceResult:
		"""
			Errors:
			- NotFoundError
			- UnhandledError
		"""

		supplier = SuppliersRepository.get_by_id(cur, supplier_id)
		if not supplier:
			return ServiceResult(error=NotFoundError(Supplier.ENTITY, Supplier.COLUMN_ID))
		return ServiceResult(result=supplier)
	
	@classmethod
	@BaseService.transaction
	def get_by_phone(
		cls,
		cur: psycopg.Cursor,
		phone: str
	) -> ServiceResult:
		"""
			Errors:
			- InvalidValueError
			- NotFoundError
			- UnhandledError
		"""

		norm_phone = Utils.normalize_phone(phone)
		if not Utils.is_valid_phone(norm_phone):
			return ServiceResult(error=InvalidValueError(Supplier.ENTITY, Supplier.COLUMN_PHONE))

		supplier = SuppliersRepository.get_by_phone(cur, norm_phone)
		if not supplier:
			return ServiceResult(error=NotFoundError(Supplier.ENTITY, Supplier.COLUMN_PHONE))
		return ServiceResult(result=supplier)
	
	@classmethod
	@BaseService.transaction
	def get_by_email(
		cls,
		cur: psycopg.Cursor,
		email: str
	) -> ServiceResult:
		"""
			Errors:
			- InvalidValueError
			- NotFoundError
			- UnhandledError
		"""

		norm_email = Utils.normalize_email(email)
		if not Utils.is_valid_email(norm_email):
			return ServiceResult(error=InvalidValueError(Supplier.ENTITY, Supplier.COLUMN_EMAIL))

		supplier = SuppliersRepository.get_by_email(cur, norm_email)
		if not supplier:
			return ServiceResult(error=NotFoundError(Supplier.ENTITY, Supplier.COLUMN_EMAIL))
		return ServiceResult(result=supplier)
	
	@classmethod
	@BaseService.transaction
	def search(
		cls,
		cur: psycopg.Cursor,
		search: str | None = None,
		limit: int = 50,
		offset: int = 0
	) -> ServiceResult:
		"""
			Errors:
			- UnhandledError
		"""

		return ServiceResult(
			result=SuppliersRepository.search(
				cur=cur,
				search=search,
				limit=limit,
				offset=offset
			)
		)
