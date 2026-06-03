import Fetch from '../../fetch.mjs';
import Cookies from '../../cookies.mjs';


export default class Suppliers {
	static URL_PREFIX = "/api/employee/suppliers";

	static Create(fullName, phone, email=null, address=null) {
		return Fetch.PostJson(
			`${Suppliers.URL_PREFIX}/create`,
			{
				full_name: fullName,
				phone, email, address
			},
			Cookies.Get('session')
		);
	}

	static Update(
		supplierId,
		fullName=null,
		phone=null,
		email=null,
		address=null
	) {
		return Fetch.PostJson(
			`${Suppliers.URL_PREFIX}/update/${supplierId}`,
			{
				full_name: fullName,
				phone, email, address
			},
			Cookies.Get('session')
		);
	}

	static Deactivate(supplierId) {
		return Fetch.PostJson(`${Suppliers.URL_PREFIX}/deactivate/${supplierId}`, null, Cookies.Get('session'));
	}

	static Restore(supplierId) {
		return Fetch.PostJson(`${Suppliers.URL_PREFIX}/restore/${supplierId}`, null, Cookies.Get('session'));
	}

	static Get(supplierId) {
		return Fetch.GetJson(`${Suppliers.URL_PREFIX}/${supplierId}`, null, Cookies.Get('session'));
	}

	static ByPhone(phone) {
		return Fetch.GetJson(`${Suppliers.URL_PREFIX}/by-phone/${phone}`, null, Cookies.Get('session'));
	}

	static ByEmail(email) {
		return Fetch.GetJson(`${Suppliers.URL_PREFIX}/by-email/${email}`, null, Cookies.Get('session'));
	}

	static Search(search, page=0) {
		return Fetch.GetJson(`${Suppliers.URL_PREFIX}/search`, {search, page}, Cookies.Get('session'));
	}
}
