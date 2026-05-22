from dataclasses import dataclass
from datetime import datetime
from app.models.public.base_model import BaseModel

@dataclass
class DbUser(BaseModel):
	id: int
	phone: str
	email: str | None
	full_name: str
	password_hash: str
	token_ver: int

	blocked_by: int | None
	blocked_at: datetime | None

	deleted_by: int | None
	deleted_at: datetime | None

	created_by: int | None
	created_at: datetime
	
	COLUMN_ID = "id"
	COLUMN_PHONE = "phone"
	COLUMN_EMAIL = "email"
	COLUMN_FULL_NAME = "full_name"
	COLUMN_TOKEN_VER = "token_ver"
	COLUMN_PASSWORD_HASH = "password_hash"
	COLUMN_BLOCKED_BY = "blocked_by"
	COLUMN_DELETED_BY = "deleted_by"
	COLUMN_CREATED_BY = "created_by"
