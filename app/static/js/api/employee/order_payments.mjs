import Fetch from '../../fetch.mjs';
import Cookies from '../../cookies.mjs';


export default class OrderPayments {
	static URL_PREFIX = "/api/employee/order_payments";

	static Get(orderPaymentId) {
		return Fetch.GetJson(`${OrderPayments.URL_PREFIX}/${orderPaymentId}`, null, Cookies.Get('session'));
	}

	static ByOrder(orderId, page=0) {
		return Fetch.GetJson(`${OrderPayments.URL_PREFIX}/by-order/${orderId}`, {page}, Cookies.Get('session'));
	}

	static IsFullyPaid(orderId) {
		return Fetch.GetJson(`${OrderPayments.URL_PREFIX}/is-fully-paid/${orderId}`, null, Cookies.Get('session'));
	}
}
