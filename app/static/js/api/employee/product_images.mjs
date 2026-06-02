import Fetch from '../../fetch.mjs';
import Cookies from '../../cookies.mjs';


export default class ProductImages {
	static URL_PREFIX = "/api/employee/product_images";

	static CreateMany(productId, images) {
		let formData = new FormData();
		for (let i = 0; i < images.length; i++) formData.append(`img-${i}`, images[i]);
		return Fetch.PostFormData(
			`${ProductImages.URL_PREFIX}/create-many/${productId}`,
			formData, Cookies.Get('session')
		);
	}

	static Delete(productImageId) {
		return Fetch.PostJson(`${ProductImages.URL_PREFIX}/delete/${productImageId}`, null, Cookies.Get('session'));
	}

	static DeleteAll(productId) {
		return Fetch.PostJson(`${ProductImages.URL_PREFIX}/delete-all/${productId}`, null, Cookies.Get('session'));
	}

	static Get(productImageId) {
		return Fetch.GetJson(`${ProductImages.URL_PREFIX}/${productImageId}`, null, Cookies.Get('session'));
	}

	static ByStorageKey(storageKey) {
		storageKey = encodeURIComponent(storageKey);
		return Fetch.GetJson(`${ProductImages.URL_PREFIX}/by-storage-key/${storageKey}`, null, Cookies.Get('session'));
	}

	static ByProduct(productId) {
		return Fetch.GetJson(`${ProductImages.URL_PREFIX}/by-product/${productId}`, null, Cookies.Get('session'));
	}

	static ByEmployee(employeeId, page=0) {
		return Fetch.GetJson(`${ProductImages.URL_PREFIX}/by-employee/${employeeId}`, {page}, Cookies.Get('session'));
	}
}
