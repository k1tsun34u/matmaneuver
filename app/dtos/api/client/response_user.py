from datetime import datetime
from dataclasses import dataclass
from app.models.db.db_user import DbUser


@dataclass
class ResponseUser:
	id: int
	phone: str
	email: str
	full_name: str
	blocked_at: datetime
	deleted_at: datetime

	def __init__(self, db_user: DbUser):
		self.id = db_user.id
		self.phone = db_user.phone
		self.email = db_user.email
		self.full_name = db_user.full_name
		self.blocked_at = db_user.blocked_at
		self.deleted_at = db_user.deleted_at
