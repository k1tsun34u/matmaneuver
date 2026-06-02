import Fetch from '../../fetch.mjs';
import Cookies from '../../cookies.mjs';


export default class Warehouses {
	static URL_PREFIX = "/api/employee/warehouses";

	static Create(address, description=null) {
		return Fetch.PostJson(
			`${Warehouses.URL_PREFIX}/create`,
			{address, description}, Cookies.Get('session')
		);
	}

	static SetDescription(warehouseId, description) {
		return Fetch.PostJson(`${Warehouses.URL_PREFIX}/set-description/${warehouseId}`, {description}, Cookies.Get('session'));
	}

	static Delete(warehouseId) {
		return Fetch.PostJson(`${Warehouses.URL_PREFIX}/delete/${warehouseId}`, null, Cookies.Get('session'));
	}

	static Restore(warehouseId) {
		return Fetch.PostJson(`${Warehouses.URL_PREFIX}/restore/${warehouseId}`, null, Cookies.Get('session'));
	}

	static Get(warehouseId) {
		return Fetch.GetJson(`${Warehouses.URL_PREFIX}/${warehouseId}`, null, Cookies.Get('session'));
	}

	static ByAddress(address) {
		address = encodeURIComponent(address);
		return Fetch.GetJson(`${Warehouses.URL_PREFIX}/by-address/${address}`, null, Cookies.Get('session'));
	}

	static Search(search, page=0, excludeDeleted=true) {
		return Fetch.GetJson(
			`${Warehouses.URL_PREFIX}/search`,
			{
				search, page,
				exclude_deleted: excludeDeleted
			},
			Cookies.Get('session')
		);
	}

	static AddProduct(warehouseId, productId) {
		return Fetch.PostJson(`${Warehouses.URL_PREFIX}/add-product/${warehouseId}/${productId}`, null, Cookies.Get('session'));
	}

	static DeleteProduct(warehouseId, productId) {
		return Fetch.PostJson(`${Warehouses.URL_PREFIX}/delete-product/${warehouseId}/${productId}`, null, Cookies.Get('session'));
	}

	static DeleteAllProducts(warehouseId) {
		return Fetch.PostJson(`${Warehouses.URL_PREFIX}/delete-all-products/${warehouseId}`, null, Cookies.Get('session'));
	}

	static IncreaseProductQuantity(warehouseId, productId, quantity) {
		return Fetch.PostJson(`${Warehouses.URL_PREFIX}/increase-product/${warehouseId}/${productId}`, {quantity}, Cookies.Get('session'));
	}

	static DecreaseProductQuantity(warehouseId, productId, quantity) {
		return Fetch.PostJson(`${Warehouses.URL_PREFIX}/decrease-product/${warehouseId}/${productId}`, {quantity}, Cookies.Get('session'));
	}

	static ReserveProduct(warehouseId, productId, quantity) {
		return Fetch.PostJson(`${Warehouses.URL_PREFIX}/reserve-product/${warehouseId}/${productId}`, {quantity}, Cookies.Get('session'));
	}

	static UnreserveProduct(warehouseId, productId, quantity) {
		return Fetch.PostJson(`${Warehouses.URL_PREFIX}/unreserve-product/${warehouseId}/${productId}`, {quantity}, Cookies.Get('session'));
	}

	static ConsumeProduct(warehouseId, productId, quantity) {
		return Fetch.PostJson(`${Warehouses.URL_PREFIX}/consume-product/${warehouseId}/${productId}`, {quantity}, Cookies.Get('session'));
	}

	static GetProductsByWarehouse(warehouseId, page=0) {
		return Fetch.GetJson(`${Warehouses.URL_PREFIX}/products/by-warehouse/${warehouseId}`, {page}, Cookies.Get('session'));
	}

	/**
	 * Получить все склады, где есть указанный товар, с полной информацией
	 * @param {number} productId - ID товара
	 * @param {number} page - Страница (0-indexed)
	 * @returns {Promise<{success: boolean, pagination: Object, products: Array<CompleteWarehouseProduct>}>}
	 */
	static GetCompleteProducts(productId, page=0) {
		return Fetch.GetJson(`${Warehouses.URL_PREFIX}/products/complete/${productId}`, {page}, Cookies.Get('session'));
	}
}
