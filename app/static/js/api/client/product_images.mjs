import Fetch from '../../fetch.mjs';


export default class ProductImages {
	static URL_PREFIX = "/api/client/product_images";

	static GetUrl(image_id) {
		return `${ProductImages.URL_PREFIX}/${image_id}`;
	}

	static ByProduct(product_id) {
		return Fetch.GetJson(
			`${ProductImages.URL_PREFIX}/by-product/${product_id}`,
			null, null
		);
	}
}
