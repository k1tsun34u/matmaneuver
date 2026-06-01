import Fetch from '../../fetch.mjs';
import Cookies from '../../cookies.mjs';


export default class Orders {
	static URL_PREFIX = "/api/client/orders";

	static Create(deliveryAddress) {
		return Fetch.PostJson(
			`${Orders.URL_PREFIX}/create`,
			{delivery_address: deliveryAddress}, Cookies.Get('session')
		);
	}

	static Pay(orderId) {
		return Fetch.PostJson(
			`${Orders.URL_PREFIX}/pay/${orderId}`,
			null, Cookies.Get('session')
		);
	}

	static Cancel(orderId) {
		return Fetch.PostJson(
			`${Orders.URL_PREFIX}/cancel/${orderId}`,
			null, Cookies.Get('session')
		);
	}

	static ByTrackNumber(trackNumber, page=0) {
		return Fetch.GetJson(
			`${Orders.URL_PREFIX}/by-track-number/${trackNumber}`,
			{page}, null
		);
	}

	static Get(orderId) {
		return Fetch.GetJson(
			`${Orders.URL_PREFIX}/${orderId}`,
			null, Cookies.Get('session')
		);
	}

	static My(page=0) {
		return Fetch.GetJson(
			`${Orders.URL_PREFIX}/my`,
			{page}, Cookies.Get('session')
		);
	}
}
