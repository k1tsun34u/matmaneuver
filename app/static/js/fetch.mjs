export default class Fetch {
	static MakeRequest(method, url, body, session) {
		let init = {
			method: method,
			headers: {
				"Content-Type": "application/json"
			}
		};

		if (body !== null) init.body = JSON.stringify(body);
		if (
			session !== undefined &&
			session !== null &&
			session !== ""
		) init.headers["Authorization"] = "Bearer " + session;
		return fetch(url, init);
	}

	static Post(url, body, session) {
		return Fetch.MakeRequest("POST", url, body, session);
	}

	static Get(url, session) {
		return Fetch.MakeRequest("GET", url, null, session);
	}
}
