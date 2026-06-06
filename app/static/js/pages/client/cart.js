import Status from '../../status.mjs';
import Carts from '../../api/client/carts.mjs';
import Products from '../../api/client/products.mjs';
import ProductImages from '../../api/client/product_images.mjs';
import CartCard from '../../components/card/cart_card.mjs';


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
				let cartCard = new CartCard(
					`/client/product/${item['product_id']}`,
					null,
					r['product']['name'],
					r['product']['price'],
					item['quantity'],
					item['product_id']
				);

				ProductImages.ByProduct(item['product_id']).then(r => {
					const images = r['images'];
					if (images.length > 0) cartCard.storageKey = images[0]['storage_key'];
				}).catch(e => Status.ShowError(e));
				elTgt.appendChild(cartCard.base);
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
