import Fetch from '../../fetch.mjs';
import Cookies from '../../cookies.mjs';


export default class Orders {
	static URL_PREFIX = "/api/employee/orders";

	static SetStatus(orderId, status) {
		return Fetch.PostJson(
			`${Orders.URL_PREFIX}/set-status/${orderId}`,
			{status}, Cookies.Get('session')
		);
	}

	static Get(orderId) {
		return Fetch.GetJson(`${Orders.URL_PREFIX}/${orderId}`, null, Cookies.Get('session'));
	}

	static ByTrackNumber(trackNumber) {
		trackNumber = encodeURIComponent(trackNumber);
		return Fetch.GetJson(`${Orders.URL_PREFIX}/by-track-number/${trackNumber}`, null, Cookies.Get('session'));
	}

	static ByUser(userId, page=0) {
		return Fetch.GetJson(`${Orders.URL_PREFIX}/by-user/${userId}`, {page}, Cookies.Get('session'));
	}

	static Search(search, page=0, status=null, createdFrom=null, createdTo=null) {
		return Fetch.GetJson(
			`${Orders.URL_PREFIX}/search`,
			{
				search, page, status,
				created_from: createdFrom,
				created_to: createdTo
			}, Cookies.Get('session')
		);
	}

	static GetTotalPrice(orderId) {
		return Fetch.GetJson(`${Orders.URL_PREFIX}/total-price/${orderId}`, null, Cookies.Get('session'));
	}

	static GetStatusHistory(orderId) {
		return Fetch.GetJson(`${Orders.URL_PREFIX}/status-history/${orderId}`, null, Cookies.Get('session'));
	}
}
