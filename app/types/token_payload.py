
from dataclasses import dataclass


@dataclass
class TokenPayload:
	user_id: int
	token_ver: int
