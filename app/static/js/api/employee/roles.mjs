import Fetch from '../../fetch.mjs';
import Cookies from '../../cookies.mjs';


export default class Roles {
	static URL_PREFIX = "/api/employee/roles";

	static Create(code, isSystem=false) {
		return Fetch.PostJson(
			`${Roles.URL_PREFIX}/create`,
			{
				code,
				is_system: isSystem
			},
			Cookies.Get('session')
		);
	}
	
	static Deactivate(roleId) {
		return Fetch.PostJson(`${Roles.URL_PREFIX}/deactivate/${roleId}`, null, Cookies.Get('session'));
	}
	
	static Restore(roleId) {
		return Fetch.PostJson(`${Roles.URL_PREFIX}/restore/${roleId}`, null, Cookies.Get('session'));
	}

	static AssignPermissions(roleId, permissionIds) {
		return Fetch.PostJson(
			`${Roles.URL_PREFIX}/assign-permissions/${roleId}`,
			{permission_ids: permissionIds}, Cookies.Get('session')
		);
	}

	static UnassignPermissions(roleId, permissionIds) {
		return Fetch.PostJson(
			`${Roles.URL_PREFIX}/unassign-permissions/${roleId}`,
			{permission_ids: permissionIds}, Cookies.Get('session')
		);
	}

	static Get(roleId) {
		return Fetch.GetJson(`${Roles.URL_PREFIX}/${roleId}`, null, Cookies.Get('session'));
	}

	static ByCode(code) {
		code = encodeURIComponent(code);
		return Fetch.GetJson(`${Roles.URL_PREFIX}/by-code/${code}`, null, Cookies.Get('session'));
	}

	static Search(search, page=0, excludeDeactivated=true) {
		return Fetch.GetJson(
			`${Roles.URL_PREFIX}/search`,
			{
				search, page,
				exclude_deactivated: excludeDeactivated
			},
			Cookies.Get('session')
		);
	}
}
