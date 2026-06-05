import Status from '../../status.mjs';
import Carts from '../../api/client/carts.mjs';
import CartProductCard from '../../components/cart_product_card.mjs';
import Products from '../../api/client/products.mjs';
import Orders from '../../api/client/orders.mjs';


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
			Products.Get(item['product_id']).then(response => {
				let product = response['product'];
				CartProductCard.RequestBuild(product, (product, me) => elTgt.appendChild(me));
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
