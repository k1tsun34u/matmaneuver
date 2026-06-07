import Orders from '../../api/client/orders.mjs';
import Carts from '../../api/client/carts.mjs';
import Status from '../../status.mjs';
import Products from '../../api/client/products.mjs';


let elProducts = document.getElementById('products');
let elAmount = document.getElementById('amount');
let elDst = document.getElementById('dst');
let elMakeOrder = document.getElementById('make_order');

let amount = 0.0;
let quantity = 0;
let products = [];
Carts.GetItems('ACTIVE', null, true).then(response => {
	let items = response['items'];

	items.forEach(item => {
		quantity += item['quantity'];
		Products.Get(item['product_id']).then(result => {
			let product = result['product'];
			let price = parseFloat(product['price']);

			products.push([
				product['id'],
				price,
				item['quantity']]
			);

			amount += price * item['quantity'];
			elAmount.innerHTML = `Итого: ${amount} ₽`;
		}).catch(error => Status.ShowError(error));
	});

	elProducts.innerHTML = `Товаров: ${quantity}`;
}).catch(error => {
	Status.ShowError(error);
	window.location.href = '/login';
});

elMakeOrder.addEventListener('click', e => {
	Orders.Create(elDst.value).then(result => {
		window.location.href = '/client/orders';
	}).catch(error => Status.ShowError(error));
});
