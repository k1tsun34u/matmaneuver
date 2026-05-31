import Fetch from '../../fetch.mjs';


export default class Products {
	static URL_PREFIX = "/api/client/products";

	static Get(product_id) {
		return Fetch.Json("GET", `${Products.URL_PREFIX}/${product_id}`, null, null);
	}

	static Search(search, minPrice, maxPrice, page=0) {
		return Fetch.GetJson(
			Products.URL_PREFIX,
			{
				search,
				min_price: minPrice,
				max_price: maxPrice,
				page
			},
			null
		);
	}
}
