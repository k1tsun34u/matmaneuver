import Fetch from '../../fetch.mjs';
import Cookies from '../../cookies.mjs';


export default class Users {
	static URL_PREFIX = "/api/employee/users";

	static Block(userId) {
		return Fetch.PostJson(`${this.URL_PREFIX}/block/${userId}`, null, Cookies.Get('session'));
	}

	static Unblock(userId) {
		return Fetch.PostJson(`${this.URL_PREFIX}/unblock/${userId}`, null, Cookies.Get('session'));
	}

	static Delete(userId) {
		return Fetch.PostJson(`${this.URL_PREFIX}/delete/${userId}`, null, Cookies.Get('session'));
	}

	static Restore(userId) {
		return Fetch.PostJson(`${this.URL_PREFIX}/restore/${userId}`, null, Cookies.Get('session'));
	}

	static Get(userId) {
		return Fetch.GetJson(`${this.URL_PREFIX}/${userId}`, null, Cookies.Get('session'));
	}

	static ByPhone(phone) {
		phone = encodeURIComponent(phone);
		return Fetch.GetJson(`${this.URL_PREFIX}/by-phone/${phone}`, null, Cookies.Get('session'));
	}

	static ByEmail(email) {
		email = encodeURIComponent(email);
		return Fetch.GetJson(`${this.URL_PREFIX}/by-email/${email}`, null, Cookies.Get('session'));
	}

	static Search(search, page=0, excludeDeleted=true, excludeBlocked=true) {
		return Fetch.GetJson(
			`${this.URL_PREFIX}/search`,
			{
				search, page,
				exclude_deleted: excludeDeleted,
				exclude_blocked: excludeBlocked
			},
			Cookies.Get('session')
		);
	}
}
