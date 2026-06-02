import Fetch from '../../fetch.mjs';
import Cookies from '../../cookies.mjs';


export default class OrderFulfillments {
	static URL_PREFIX = "/api/employee/order_fulfillments";

	/**
	 * @param {number} orderId - ID заказа
	 * @param {Array<[number, Array<[number, number]>]>} fulfillmentsData 
	 *        Формат: [[warehouse_id, [product_id, quantity], ...], ...]
	 * @returns {Promise<{success: boolean, fulfillments: Array<{id: number, items: number[]}>}>}
	 */
	static Create(orderId, fulfillmentsData) {
		return Fetch.PostJson(
			`${OrderFulfillments.URL_PREFIX}/create/${orderId}`,
			{fulfillments_data: fulfillmentsData}, Cookies.Get('session')
		);
	}

	static Get(orderFulfillmentId) {
		return Fetch.GetJson(`${OrderFulfillments.URL_PREFIX}/${orderFulfillmentId}`, null, Cookies.Get('session'));
	}

	static ByOrder(orderId, page=0) {
		return Fetch.GetJson(`${OrderFulfillments.URL_PREFIX}/by-order/${orderId}`, {page}, Cookies.Get('session'));
	}

	static ByWarehouse(warehouseId, page=0) {
		return Fetch.GetJson(`${OrderFulfillments.URL_PREFIX}/by-warehouse/${warehouseId}`, {page}, Cookies.Get('session'));
	}

	static GetItem(orderFulfillmentItemId) {
		return Fetch.GetJson(`${OrderFulfillments.URL_PREFIX}/item/${orderFulfillmentItemId}`, null, Cookies.Get('session'));
	}

	static GetItemsByOrderFulfillment(orderFulfillmentId, page=0) {
		return Fetch.GetJson(`${OrderFulfillments.URL_PREFIX}/items/by-order-fulfillment/${orderFulfillmentId}`, {page}, Cookies.Get('session'));
	}

	static GetItemsByProduct(productId, page=0) {
		return Fetch.GetJson(`${OrderFulfillments.URL_PREFIX}/items/by-product/${productId}`, {page}, Cookies.Get('session'));
	}

	static GetFulfilledQuantity(orderId, productId) {
		return Fetch.GetJson(`${OrderFulfillments.URL_PREFIX}/fulfilled-quantity/${orderId}/${productId}`, null, Cookies.Get('session'));
	}
}
