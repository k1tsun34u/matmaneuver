import Fetch from '../../fetch.mjs';
import Cookies from '../../cookies.mjs';


export default class WriteOffs {
	static URL_PREFIX = "/api/employee/write_offs";
	
	/**
	 * Создание списания товаров
	 * @param {number} warehouseId - ID склада
	 * @param {string} reason - Причина списания (damaged, expired, defective, etc.)
	 * @param {Array<[number, number]>} writeOffsData - Массив [product_id, quantity]
	 * @param {string|null} comment - Комментарий (опционально)
	 * @example
	 * const items = [[100, 5], [200, 3]];  // списать 5 шт товара 100 и 3 шт товара 200
	 * await WriteOffs.Create(1, 'damaged', items, 'Повреждено при транспортировке');
	 */
	static Create(warehouseId, reason, writeOffsData, comment=null) {
		return Fetch.PostJson(
			`${WriteOffs.URL_PREFIX}/create/${warehouseId}`,
			{
				reason, comment,
				write_offs_data: writeOffsData
			},
			Cookies.Get('session')
		);
	}

	static Get(writeOffId) {
		return Fetch.GetJson(`${WriteOffs.URL_PREFIX}/${writeOffId}`, null, Cookies.Get('session'));
	}

	static ByWarehouse(warehouseId, page=0) {
		return Fetch.GetJson(`${WriteOffs.URL_PREFIX}/by-warehouse/${warehouseId}`, {page}, Cookies.Get('session'));
	}

	static Search(
		search, page=0,
		warehouseId=null,
		reason=null,
		createdFrom=null, createdTo=null
	) {
		return Fetch.GetJson(
			`${WriteOffs.URL_PREFIX}/search`,
			{
				search, reason, page,
				warehouse_id: warehouseId,
				created_from: createdFrom,
				created_to: createdTo
			},
			Cookies.Get('session')
		);
	}

	static GetItem(writeOffItemId) {
		return Fetch.GetJson(`${WriteOffs.URL_PREFIX}/item/${writeOffItemId}`, null, Cookies.Get('session'));
	}

	static GetItemsByWriteOff(writeOffId, page=0) {
		return Fetch.GetJson(`${WriteOffs.URL_PREFIX}/items/by-write-off/${writeOffId}`, {page}, Cookies.Get('session'));
	}

	static GetItemsByProduct(productId, page=0) {
		return Fetch.GetJson(`${WriteOffs.URL_PREFIX}/items/by-product/${productId}`, {page}, Cookies.Get('session'));
	}
}
