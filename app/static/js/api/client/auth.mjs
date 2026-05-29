import Cookies from '../../cookies.mjs';
import Status from '../../status.mjs';
import Fetch from '../../fetch.mjs';


export default class Auth {
	static URL_PREFIX = "/api/client/auth";

	static Login(phone, email, password) {
		let body = {
			phone: phone,
			password: password
		};

		if (email) body.email = email;
		Fetch.Post(`${Auth.URL_PREFIX}/login`, body).then(async response => {
			const data = await response.json();
			if (!response.ok) Status.ShowError(data.error);
			else {
				Cookies.Set('session', data.session);
				window.location.href = '/client/profile';
			}
		}).catch(error => Status.ShowError(error.message));
	}

	static Register(phone, email, full_name, password) {
		let body = {
			phone: phone,
			full_name: full_name,
			password: password
		};

		if (email) body.email = email;
		Fetch.Post(`${Auth.URL_PREFIX}/register`, body).then(async response => {
			const data = await response.json();
			if (!response.ok) Status.ShowError(data.error);
			else {
				Cookies.Set('session', data.session);
				window.location.href = '/client/profile';
			}
		}).catch(error => Status.ShowError(error.message));
	}

	static Update(phone, email, full_name) {
		let body = {};
		if (phone !== undefined) body.phone = phone;
		if (email !== undefined) body.email = email;
		if (full_name !== undefined) body.full_name = full_name;
		
		Fetch.Post(`${Auth.URL_PREFIX}/update`, body, Cookies.Get("session")).then(async response => {
			const data = await response.json();
			if (!response.ok) Status.ShowError(data.error);
			else window.location.href = '/client/profile';
		}).catch(error => Status.ShowError(error.message));
	}

	static SetPassword(password) {
		let body = {password: password};
		Fetch.Post(`${Auth.URL_PREFIX}/set-password`, body, Cookies.Get("session")).then(async response => {
			const data = await response.json();
			if (!response.ok) Status.ShowError(data.error);
			else {
				Cookies.Set('session', data.session);
				window.location.href = '/client/profile';
			}
		}).catch(error => Status.ShowError(error.message));
	}

	static Me(dispatcher) {
		Fetch.Get(`${Auth.URL_PREFIX}/me`, Cookies.Get("session")).then(async response => {
			const data = await response.json();
			if (!response.ok) Status.ShowError(data.error);
			else dispatcher(data);
		}).catch(error => Status.ShowError(error.message));
	}
}
