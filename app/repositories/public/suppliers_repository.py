import psycopg
from typing import ClassVar
from app.models.db.db_user import DbUser
from app.models.public.employee import Employee
from app.models.public.supplier_employee import SupplierEmployee
from app.utils import Utils
from app.unset import Unset, UNSET
from app.models.public.supplier import Supplier
from app.types.update_result import UpdateResult
from app.repositories.base.base_repository import BaseRepository
from app.repositories.base.mixins.updatable_mixin import UpdatableMixin
from app.repositories.base.mixins.selectable_mixin import SelectableMixin
from app.repositories.base.mixins.audit_state_mixin import AuditStateMixin


class SuppliersRepository(
	BaseRepository,
	AuditStateMixin,
	UpdatableMixin,
	SelectableMixin[Supplier]
):
	TABLE: ClassVar[str] = Supplier.TABLE
	MODEL = Supplier
	TABLE_COLUMNS = (
		Supplier.COLUMN_ID,
		Supplier.COLUMN_FULL_NAME,
		Supplier.COLUMN_PHONE,
		Supplier.COLUMN_EMAIL,
		Supplier.COLUMN_ADDRESS,
		Supplier.COLUMN_DEACTIVATED_BY,
		Supplier.COLUMN_DEACTIVATED_AT,
		Supplier.COLUMN_CREATED_BY,
		Supplier.COLUMN_CREATED_AT,
	)

	ORDER_BY = ((Supplier.COLUMN_CREATED_AT, "DESC",),)

	@classmethod
	def create(
		cls,
		cur: psycopg.Cursor,
		full_name: str,
		phone: str,
		email: str | None,
		address: str | None,
		created_by: int | None
	) -> int:
		return cls.execute_create(
			cur=cur,
			table=cls.TABLE,
			fields={
				Supplier.COLUMN_FULL_NAME: full_name,
				Supplier.COLUMN_PHONE: phone,
				Supplier.COLUMN_EMAIL: email,
				Supplier.COLUMN_ADDRESS: address,
				Supplier.COLUMN_CREATED_BY: created_by
			},
			returning=Supplier.COLUMN_ID
		)[Supplier.COLUMN_ID]
	
	@classmethod
	def update(
		cls,
		cur: psycopg.Cursor,
		supplier_id: int,
		full_name: str | Unset = UNSET,
		phone: str | Unset = UNSET,
		email: str | None | Unset = UNSET,
		address: str | None | Unset = UNSET
	) -> UpdateResult:
		return cls.update_by_conditions(
			cur=cur,
			identity_where={Supplier.COLUMN_ID: supplier_id},
			condition_where={},
			fields=Utils.filter_unset({
				Supplier.COLUMN_FULL_NAME: full_name,
				Supplier.COLUMN_PHONE: phone,
				Supplier.COLUMN_EMAIL: email,
				Supplier.COLUMN_ADDRESS: address
			})
		)
	
	@classmethod
	def deactivate(cls, cur: psycopg.Cursor, supplier_id: int, deactivated_by: int | None) -> UpdateResult:
		return cls.set_state(cur, "deactivated", {Supplier.COLUMN_ID: supplier_id}, deactivated_by)
	
	@classmethod
	def restore(cls, cur: psycopg.Cursor, supplier_id: int) -> UpdateResult:
		return cls.clear_state(cur, "deactivated", {Supplier.COLUMN_ID: supplier_id})
	
	@classmethod
	def get_by_id(cls, cur: psycopg.Cursor, supplier_id: int) -> SupplierEmployee | None:
		query = f"""
			SELECT 
				s.*,
				u_deactivator.{DbUser.COLUMN_FULL_NAME} AS deactivated_by_{DbUser.COLUMN_FULL_NAME}
			FROM {Supplier.TABLE} AS s
			LEFT JOIN {Employee.TABLE} AS e_deactivator ON e_deactivator.{Employee.COLUMN_ID} = s.{Supplier.COLUMN_DEACTIVATED_BY}
			LEFT JOIN {DbUser.TABLE} AS u_deactivator ON u_deactivator.{DbUser.COLUMN_ID} = e_deactivator.{Employee.COLUMN_USER_ID}
			WHERE s.{Supplier.COLUMN_ID} = %s
		"""
		cur.execute(query, (supplier_id,))
		row = cur.fetchone()
		return SupplierEmployee(**row) if row else None
	
	@classmethod
	def get_by_phone(cls, cur: psycopg.Cursor, phone: str) -> Supplier | None:
		return cls.select(cur, {Supplier.COLUMN_PHONE: phone})
	
	@classmethod
	def get_by_email(cls, cur: psycopg.Cursor, email: str) -> Supplier | None:
		return cls.select(cur, {Supplier.COLUMN_EMAIL: email})
	
	@classmethod
	def search(
		cls,
		cur: psycopg.Cursor,
		search: str | None = None,
		limit: int = 50,
		offset: int = 0
	) -> tuple[list[Supplier], int]:
		ilike = (
			(
				Supplier.COLUMN_FULL_NAME,
				Supplier.COLUMN_PHONE,
				Supplier.COLUMN_EMAIL,
				Supplier.COLUMN_ADDRESS,
			),
			f"%{search}%",
		) if search else None

		suppliers = cls.select_many(
			cur=cur,
			ilike=ilike,
			limit=limit,
			offset=offset
		)

		conditions, params = Utils.build_conditions_params(
			ilike=ilike
		)

		query = f"""
			SELECT COUNT(*) as total
			FROM {cls.TABLE}
			{Utils.build_where(conditions)}
		"""
		cur.execute(query, params)
		return (suppliers, cur.fetchone()['total'],)
