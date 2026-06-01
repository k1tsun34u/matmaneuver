import Fetch from '../../fetch.mjs';
import Cookies from '../../cookies.mjs';


export default class Products {
	static URL_PREFIX = "/api/employee/products";

	static Create(name, price, description=null) {
		return Fetch.PostJson(
			`${Products.URL_PREFIX}/create`,
			{name, description, price}, Cookies.Get('session')
		);
	}

	static SetDescription(productId, description) {
		return Fetch.PostJson(`${Products.URL_PREFIX}/set-description/${productId}`, {description}, Cookies.Get('session'));
	}

	static SetPrice(productId, price) {
		return Fetch.PostJson(`${Products.URL_PREFIX}/set-price/${productId}`, {price}, Cookies.Get('session'));
	}

	static Delete(productId) {
		return Fetch.PostJson(`${Products.URL_PREFIX}/delete/${productId}`, null, Cookies.Get('session'));
	}

	static Restore(productId) {
		return Fetch.PostJson(`${Products.URL_PREFIX}/restore/${productId}`, null, Cookies.Get('session'));
	}

	static Get(productId) {
		return Fetch.GetJson(`${Products.URL_PREFIX}/${productId}`, null, Cookies.Get('session'));
	}

	static ByEmployee(employeeId, page=0, excludeDeleted=true) {
		return Fetch.GetJson(
			`${Products.URL_PREFIX}/by-employee/${employeeId}`,
			{
				page,
				exclude_deleted: excludeDeleted
			},
			Cookies.Get('session')
		);
	}

	static Search(search, page=0, minPrice=null, maxPrice=null, excludeDeleted=true) {
		return Fetch.GetJson(
			`${Products.URL_PREFIX}/search`,
			{
				search, page,
				min_price: minPrice,
				max_price: maxPrice,
				exclude_deleted: excludeDeleted
			},
			Cookies.Get('session')
		);
	}
}
