import Status from '../../status.mjs';
import Carts from '../../api/client/carts.mjs';
import Products from '../../api/client/products.mjs';
import CartItemBar from '../../components/cart_item_bar.mjs';
import ProductImages from '../../api/client/product_images.mjs';


let elTgt = document.getElementById('tgt');
let elMakeOrder = document.getElementById('make_order');

Carts.GetItems('ACTIVE').then(result => {
	const items = result['items'];
	const len = items.length;
	if (len <= 0) {
		elMakeOrder.style.cursor = 'not-allowed';
		elMakeOrder.style.background = 'gray';
	}
	else {
		elTgt.innerHTML = '';
		items.forEach(item => {
			Products.Get(item['product_id']).then(r => {
				let cartItemBar = new CartItemBar(
					item['product_id'],
					null,
					r['product']['name'],
					r['product']['price'],
					item['quantity'],
					'ACTIVE'
				);

				// ProductImages.ByProduct(item['product_id']).then(r => {
				// 	const images = r['images'];
				// 	if (images.length > 0) cartItemCard.setImg(images[0]['storage_key']);
				// }).catch(e => Status.ShowError(e));
				elTgt.appendChild(cartItemBar.base);
			}).catch(error => Status.ShowError(error));
		});

		elMakeOrder.addEventListener('click', e => {
			window.location.href = '/client/make-order';
		});
	}
}).catch(error => {
	Status.ShowError(error);
	window.location.href = '/login';
});
