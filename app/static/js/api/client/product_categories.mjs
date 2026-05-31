import Fetch from '../../fetch.mjs';


export default class ProductCategories {
	static URL_PREFIX = "/api/client/product_categories";

	static ByProduct(productId) {
		return Fetch.GetJson(
			`${ProductCategories.URL_PREFIX}/by-product/${productId}`,
			null, null
		);
	}

	static ByCategory(categoryId, page, dispatcher) {
		return Fetch.GetJson(
			`${ProductCategories.URL_PREFIX}/by-category/${categoryId}?page=${page}`,
			null, null
		);
	}
}
