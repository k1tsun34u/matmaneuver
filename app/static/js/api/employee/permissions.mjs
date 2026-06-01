import Fetch from '../../fetch.mjs';
import Cookies from '../../cookies.mjs';


export default class Permissions {
	static URL_PREFIX = "/api/employee/permissions";

	static Create(code, description=null, isSystem=false) {
		return Fetch.PostJson(
			`${Permissions.URL_PREFIX}/create`,
			{
				code, description,
				is_system: isSystem
			},
			Cookies.Get('session')
		);
	}
	
	static SetDescription(permissionId, description) {
		return Fetch.PostJson(
			`${Permissions.URL_PREFIX}/set-description/${permissionId}`,
			{description}, Cookies.Get('session')
		);
	}
	
	static Deactivate(permissionId) {
		return Fetch.PostJson(`${Permissions.URL_PREFIX}/deactivate/${permissionId}`, null, Cookies.Get('session'));
	}
	
	static Restore(permissionId) {
		return Fetch.PostJson(`${Permissions.URL_PREFIX}/restore/${permissionId}`, null, Cookies.Get('session'));
	}

	static Get(permissionId) {
		return Fetch.GetJson(`${Permissions.URL_PREFIX}/${permissionId}`, null, Cookies.Get('session'));
	}

	static ByCode(code) {
		return Fetch.GetJson(`${Permissions.URL_PREFIX}/by-code/${code}`, null, Cookies.Get('session'));
	}

	static Search(search, page=0, excludeDeactivated=true) {
		return Fetch.GetJson(
			`${Permissions.URL_PREFIX}/search`,
			{
				search, page,
				exclude_deactivated: excludeDeactivated
			},
			Cookies.Get('session')
		);
	}
}
