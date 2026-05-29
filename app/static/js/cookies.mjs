export default class Cookies {
	static EXPIRE_DAYS = 30;

	static Get(cname) {
		let name = cname + "=";
		let decodedCookie = decodeURIComponent(document.cookie);
		let ca = decodedCookie.split(';');
		
		for(let i = 0; i < ca.length; i++) {
			let c = ca[i];
			while (c.charAt(0) == ' ') c = c.substring(1);
			if (c.indexOf(name) == 0) return c.substring(name.length, c.length);
		}

		return "";
	}

	static Set(cname, cvalue) {
		const d = new Date();
		d.setTime(d.getTime() + (Cookies.EXPIRE_DAYS * 24 * 60 * 60 * 1000));

		let expires = "expires="+ d.toUTCString();
		document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
	}
}
