import Fetch from '../../fetch.mjs';
import Cookies from '../../cookies.mjs';


export default class ProductReviews {
	static URL_PREFIX = "/api/employee/product_reviews";

	static Delete(productId, userId) {
		return Fetch.PostJson(`${ProductReviews.URL_PREFIX}/delete/${productId}/${userId}`, null, Cookies.Get('session'));
	}

	static DeleteAllByProduct(productId) {
		return Fetch.PostJson(`${ProductReviews.URL_PREFIX}/by-product/${productId}/delete-all`, null, Cookies.Get('session'));
	}

	static DeleteAllByUser(userId) {
		return Fetch.PostJson(`${ProductReviews.URL_PREFIX}/by-user/${userId}/delete-all`, null, Cookies.Get('session'));
	}

	static ByProduct(productId, page=0) {
		return Fetch.GetJson(`${ProductReviews.URL_PREFIX}/by-product/${productId}`, {page}, Cookies.Get('session'));
	}

	static ByUser(userId, page=0) {
		return Fetch.GetJson(`${ProductReviews.URL_PREFIX}/by-user/${userId}`, {page}, Cookies.Get('session'));
	}

	static GetRating(productId) {
		return Fetch.GetJson(`${ProductReviews.URL_PREFIX}/rating/${productId}`, null, Cookies.Get('session'));
	}
}
