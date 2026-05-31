import Cookies from '../../cookies.mjs';
import Fetch from '../../fetch.mjs';


export default class ProductReviews {
	static URL_PREFIX = "/api/client/product_reviews";

	static Create(product_id, rating, comment=null) {
		let body = {
			product_id,
			rating,
			comment
		};

		return Fetch.PostJson(
			`${ProductReviews.URL_PREFIX}/create`,
			body, Cookies.Get('session')
		);
	}

	static Delete(product_id) {
		return Fetch.DeleteJson(
			`${ProductReviews.URL_PREFIX}/delete`,
			{product_id}, Cookies.Get('session')
		);
	}

	static ByProduct(product_id, page=0) {
		return Fetch.GetJson(
			`${ProductReviews.URL_PREFIX}/by-product/${product_id}`,
			{page}, null
		);
	}

	static ByUser(user_id, page=0) {
		return Fetch.GetJson(
			`${ProductReviews.URL_PREFIX}/by-user/${user_id}`,
			{page}, null
		);
	}

	static GetRating(product_id) {
		return Fetch.GetJson(
			`${ProductReviews.URL_PREFIX}/rating/${product_id}`,
			null, null
		);
	}
}
