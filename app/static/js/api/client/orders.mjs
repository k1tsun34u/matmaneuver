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

	static Pay(orderId, amount) {
		// warning: TODO: temporary solution
		return Fetch.PostJson(`${Orders.URL_PREFIX}/pay/${orderId}`, {amount}, Cookies.Get('session'));
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
}
