from typing import ClassVar
from datetime import datetime
from dataclasses import dataclass
from app.models.public.base_model import BaseModel

@dataclass
class DbUser(BaseModel):
	COLUMN_ID: ClassVar[str] = "id"
	COLUMN_PHONE: ClassVar[str] = "phone"
	COLUMN_EMAIL: ClassVar[str] = "email"
	COLUMN_FULL_NAME: ClassVar[str] = "full_name"
	COLUMN_TOKEN_VER: ClassVar[str] = "token_ver"
	COLUMN_PASSWORD_HASH: ClassVar[str] = "password_hash"
	COLUMN_BLOCKED_BY: ClassVar[str] = "blocked_by"
	COLUMN_BLOCKED_AT: ClassVar[str] = "blocked_at"
	COLUMN_DELETED_BY: ClassVar[str] = "deleted_by"
	COLUMN_DELETED_AT: ClassVar[str] = "deleted_at"
	COLUMN_CREATED_BY: ClassVar[str] = "created_by"
	COLUMN_CREATED_AT: ClassVar[str] = "created_at"

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
