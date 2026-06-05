import Fetch from '../../fetch.mjs';
import Cookies from '../../cookies.mjs';


export default class Carts {
	static URL_PREFIX = "/api/client/carts";

	static Add(cart_type, product_id) {
		return Fetch.PostJson(
			`${Carts.URL_PREFIX}/add-item`,
			{cart_type, product_id}, Cookies.Get('session')
		);
	}

	static Dec(cart_type, product_id) {
		return Fetch.PostJson(
			`${Carts.URL_PREFIX}/dec-item`,
			{cart_type, product_id}, Cookies.Get('session')
		);
	}

	static RemoveItem(cart_type, product_id) {
		return Fetch.PostJson(
			`${Carts.URL_PREFIX}/remove-item`,
			{cart_type, product_id}, Cookies.Get('session')
		);
	}

	static RemoveItems(cart_type) {
		return Fetch.PostJson(
			`${Carts.URL_PREFIX}/remove-items`,
			{cart_type}, Cookies.Get('session')
		);
	}

	static GetItems(cart_type, page=null, allItems=true) {
		return Fetch.GetJson(
			`${Carts.URL_PREFIX}/${cart_type}`,
			{page, all_items: allItems}, Cookies.Get('session')
		);
	}
}
