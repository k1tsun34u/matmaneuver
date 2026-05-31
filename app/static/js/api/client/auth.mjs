import Cookies from '../../cookies.mjs';
import Status from '../../status.mjs';
import Fetch from '../../fetch.mjs';


export default class Auth {
	static URL_PREFIX = "/api/client/auth";

	static async Login(phone, email, password) {
		let body = {password: password};
		if (phone) body.phone = phone;
		if (email) body.email = email;

		const data = await Fetch.PostJson(`${Auth.URL_PREFIX}/login`, body, null);
		Cookies.Set('session', data.session);
		window.location.href = '/client/profile';
	}

	static async Register(phone, email, full_name, password) {
		let body = {
			phone: phone,
			full_name: full_name,
			password: password
		};

		if (email) body.email = email;

		const data = await Fetch.PostJson(`${Auth.URL_PREFIX}/register`, body, null);
		Cookies.Set('session', data.session);
		window.location.href = '/client/profile';
	}

	static async Update(phone, email, full_name) {
		let body = {};
		if (phone !== undefined && phone.length > 0) body.phone = phone;
		if (email !== undefined && email.length > 0) body.email = email;
		if (full_name !== undefined && full_name.length > 0) body.full_name = full_name;
		
		await Fetch.PostJson(`${Auth.URL_PREFIX}/update`, body, Cookies.Get("session"));
		window.location.href = '/client/profile';
	}

	static async SetPassword(password) {
		let body = {password: password};
		
		const data = await Fetch.PostJson(`${Auth.URL_PREFIX}/set-password`, body, Cookies.Get("session"));
		Cookies.Set('session', data.session);
		window.location.href = '/client/profile';
	}

	static Me() {
		return Fetch.GetJson(`${Auth.URL_PREFIX}/me`, null, Cookies.Get("session"));
	}
}
