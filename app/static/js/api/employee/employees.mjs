import Fetch from '../../fetch.mjs';
import Cookies from '../../cookies.mjs';


export default class Employees {
	static URL_PREFIX = "/api/employee/employees";

	static async Login(phone, email, password) {
		let body = {password: password};
		if (phone) body.phone = phone;
		if (email) body.email = email;

		const data = await Fetch.PostJson("/api/client/auth/login", body, null);
		Cookies.Set('session', data.session);
		return data;
	}

	static Register(userId, hiredAt) {
		let body = {
			user_id: userId,
			hired_at: hiredAt
		};

		return Fetch.PostJson(`${Employees.URL_PREFIX}/register`, body, Cookies.Get('session'));
	}

	static Fire(tgtEmpId) {
		return Fetch.PostJson(`${Employees.URL_PREFIX}/fire/${tgtEmpId}`, null, Cookies.Get('session'));
	}

	static Rehire(tgtEmpId) {
		return Fetch.PostJson(`${Employees.URL_PREFIX}/rehire/${tgtEmpId}`, null, Cookies.Get('session'));
	}

	static AssignRoles(tgtEmpId, roleIds) {
		return Fetch.PostJson(
			`${Employees.URL_PREFIX}/assign-roles/${tgtEmpId}`,
			{role_ids: roleIds}, Cookies.Get('session')
		);
	}

	static UnassignRoles(tgtEmpId, roleIds) {
		return Fetch.PostJson(
			`${Employees.URL_PREFIX}/unassign-roles/${tgtEmpId}`,
			{role_ids: roleIds}, Cookies.Get('session')
		);
	}

	static Get(tgtEmpId) {
		return Fetch.GetJson(`${Employees.URL_PREFIX}/${tgtEmpId}`, null, Cookies.Get('session'));
	}

	static ByUser(userId) {
		return Fetch.GetJson(`${Employees.URL_PREFIX}/by-user/${userId}`, null, Cookies.Get('session'));
	}

	static Search(search, page=0) {
		return Fetch.GetJson(
			`${Employees.URL_PREFIX}/search`,
			{search, page}, Cookies.Get('session')
		);
	}

	static GetRoles(tgtEmpId) {
		return Fetch.GetJson(`${Employees.URL_PREFIX}/roles/${tgtEmpId}`, null, Cookies.Get('session'));
	}

	static GetPermissions(tgtEmpId) {
		return Fetch.GetJson(`${Employees.URL_PREFIX}/permissions/${tgtEmpId}`, null, Cookies.Get('session'));
	}

	static Me() {
		return Fetch.GetJson(`${Employees.URL_PREFIX}/me`, null, Cookies.Get('session'));
	}
}
