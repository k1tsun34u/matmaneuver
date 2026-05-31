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

	static async Json(method, url, body, session=null) {
		const response = await Fetch.MakeRequest(method, url, body, session);
		let data = null;

		try {data = await response.json();}
		catch {}
		if (!response.ok) throw new Error(data?.error ?? "Неизвестная ошибка");
		return data;
	}

	static GetJson(url, args, session=null) {
		if (args) {
			args = Object.fromEntries(Object.entries(args).filter(([_, v]) => v !== null && v !== undefined));
			if (Object.keys(args).length > 0) url += `?${new URLSearchParams(args)}`;
		}

		return Fetch.Json("GET", url, null, session);
	}

	static PostJson(url, body, session=null) {
		return Fetch.Json("POST", url, body, session);
	}

	static DeleteJson(url, body, session=null) {
		return Fetch.Json("DELETE", url, body, session);
	}
}
