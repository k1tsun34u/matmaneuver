import Fetch from '../../fetch.mjs';
import Cookies from '../../cookies.mjs';


export default class OrderPayments {
	static URL_PREFIX = "/api/client/order_payments";

	static Create(orderId, amount, paymentMethod=null) {
		return Fetch.PostJson(
			`${OrderPayments.URL_PREFIX}/create/${orderId}`,
			{amount, payment_method: paymentMethod}, Cookies.Get('session')
		);
	}

	static ByOrder(orderId, page=0) {
		return Fetch.GetJson(
			`${OrderPayments.URL_PREFIX}/by-order/${orderId}`,
			{page}, Cookies.Get('session')
		);
	}

	static My(page=0) {
		return Fetch.GetJson(`${OrderPayments.URL_PREFIX}/my`, {page}, Cookies.Get('session'));
	}
}
