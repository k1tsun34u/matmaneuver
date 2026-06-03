import Fetch from '../../fetch.mjs';
import Cookies from '../../cookies.mjs';


export default class Supplies {
	static URL_PREFIX = "/api/employee/supplies";

	/**
	 * Создание поставок
	 * @param {number} supplierId - ID поставщика
	 * @param {Array<[number, string, Array<[number, number]>]>} suppliesData 
	 *        Формат: [[warehouse_id, planned_delivery_date, [product_id, quantity], ...], ...]
	 * @example
	 * const data = [
	 *   [1, "2025-03-25", [100, 10], [200, 5]],  // склад 1, дата, товар 100 (10 шт), товар 200 (5 шт)
	 *   [2, "2025-03-26", [300, 7]]               // склад 2, дата, товар 300 (7 шт)
	 * ];
	 * await Supplies.Create(123, data);
	 */
	static Create(supplierId, suppliesData) {
		return Fetch.PostJson(
			`${Supplies.URL_PREFIX}/create/${supplierId}`,
			{supplies_data: suppliesData}, Cookies.Get('session')
		);
	}

	static SetStatus(supplyId, status) {
		return Fetch.PostJson(`${Supplies.URL_PREFIX}/set-status/${supplyId}`, {status}, Cookies.Get('session'));
	}

	static Get(supplyId) {
		return Fetch.GetJson(`${Supplies.URL_PREFIX}/${supplyId}`, null, Cookies.Get('session'));
	}

	static BySupplier(supplierId, page=0) {
		return Fetch.GetJson(`${Supplies.URL_PREFIX}/by-supplier/${supplierId}`, {page}, Cookies.Get('session'));
	}

	static ByWarehouse(warehouseId, page=0) {
		return Fetch.GetJson(`${Supplies.URL_PREFIX}/by-warehouse/${warehouseId}`, {page}, Cookies.Get('session'));
	}

	static Search(
		status, page=0,
		createdFrom=null, createdTo=null,
		plannedDeliveryDateFrom=null, plannedDeliveryDateTo=null,
	) {
		return Fetch.GetJson(
			`${Supplies.URL_PREFIX}/search`,
			{
				status, page,
				created_from: createdFrom,
				created_to: createdTo,
				planned_delivery_from: plannedDeliveryDateFrom,
				planned_delivery_to: plannedDeliveryDateTo,
			},
			Cookies.Get('session')
		);
	}

	static GetItem(supplyItemId) {
		return Fetch.GetJson(`${Supplies.URL_PREFIX}/item/${supplyItemId}`, null, Cookies.Get('session'));
	}

	static GetItemsBySupply(supplyId, page=0) {
		return Fetch.GetJson(`${Supplies.URL_PREFIX}/items/by-supply/${supplyId}`, {page}, Cookies.Get('session'));
	}

	static GetItemsByProduct(productId, page=0) {
		return Fetch.GetJson(`${Supplies.URL_PREFIX}/items/by-product/${productId}`, {page}, Cookies.Get('session'));
	}

	static GetTotalPrice(supplyId) {
		return Fetch.GetJson(`${Supplies.URL_PREFIX}/total-price/${supplyId}`, null, Cookies.Get('session'));
	}

	static GetStatusHistory(supplyId, page=0) {
		return Fetch.GetJson(`${Supplies.URL_PREFIX}/status-history/${supplyId}`, {page}, Cookies.Get('session'));
	}
}
