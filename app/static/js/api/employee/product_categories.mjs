import Fetch from '../../fetch.mjs';
import Cookies from '../../cookies.mjs';


export default class ProductCategories {
	static URL_PREFIX = "/api/employee/product_categories";

	static AssignMany(productId, categoryIds) {
		return Fetch.PostJson(
			`${ProductCategories.URL_PREFIX}/assign-many/${productId}`,
			{category_ids: categoryIds}, Cookies.Get('session')
		);
	}

	static UnassignMany(productId, categoryIds) {
		return Fetch.PostJson(
			`${ProductCategories.URL_PREFIX}/unassign-many/${productId}`,
			{category_ids: categoryIds}, Cookies.Get('session')
		);
	}
	
	static ByProduct(productId) {
		return Fetch.GetJson(`${ProductCategories.URL_PREFIX}/by-product/${productId}`, null, Cookies.Get('session'));
	}
}
