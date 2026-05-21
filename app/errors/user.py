

class UserPhoneAlreadyExistsError(Exception):
	def __init__(self, phone: str):
		self.phone = phone
		super().__init__(f"User with phone {phone} already exists")


class UserEmailAlreadyExistsError(Exception):
	def __init__(self, email: str):
		self.email = email
		super().__init__(f"User with email {email} already exists")


class UserNotFoundError(Exception):
	def __init__(self, user_id: int):
		self.user_id = user_id
		super().__init__(f"User with id {user_id} not found")


class EmployeeNotFoundError(Exception):
	def __init__(self, employee_id: int):
		self.employee_id = employee_id
		super().__init__(f"Employee with id {employee_id} not found")


class EmployeeNotFoundByUserError(Exception):
	def __init__(self, user_id: int):
		self.employee_id = user_id
		super().__init__(f"Employee with user id {user_id} not found")


class EmployeeAlreadyExistsError(Exception):
	def __init__(self, employee_id: int):
		self.employee_id = employee_id
		super().__init__(f"Employee with id {employee_id} already exists")


class RoleCodeAlreadyExistsError(Exception):
	def __init__(self, code: str):
		self.code = code
		super().__init__(f"Role with code {code} already exists")


class RoleNotFoundError(Exception):
	def __init__(self, role_id: int):
		self.role_id = role_id
		super().__init__(f"Role with id {role_id} not found")


class PermissionCodeAlreadyExistsError(Exception):
	def __init__(self, code: str):
		self.code = code
		super().__init__(f"Permission with code {code} already exists")


class PermissionNotFoundError(Exception):
	def __init__(self, permission_id: int):
		self.permission_id = permission_id
		super().__init__(f"Permission with id {permission_id} not found")
