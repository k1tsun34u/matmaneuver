import Products from '../api/client/products.mjs'
import Status from '../status.mjs';


export default class OrderItemBar {
	static RequestBuild(item, callback) {
		Products.Get(item['product_id']).then(response => {
			let product = response['product'];
			let fnRedirect = (e) => {window.location.href = `/client/product/${item['product_id']}`;}

			let res = document.createElement('div');
			res.classList.add('hcont');
			res.style.cursor = 'pointer';
			res.addEventListener('click', fnRedirect);

			let number = document.createElement('p');
			let name = document.createElement('p');
			name.classList.add('order-item-name');

			let purchasePrice = document.createElement('p');
			let quantity = document.createElement('p');

			number.innerHTML = `#${item['id']}`;
			name.innerHTML = product['name'];
			purchasePrice.innerHTML = `${item['price']}₽/шт`;
			quantity.innerHTML = `${item['quantity']} шт`;

			number.style.maxWidth = '7%';
			purchasePrice.style.color = '#21c800';
			quantity.style.color = '#0065df';

			number.addEventListener('click', fnRedirect);
			purchasePrice.addEventListener('click', fnRedirect);
			quantity.addEventListener('click', fnRedirect);

			res.appendChild(number);
			res.appendChild(name);
			res.appendChild(purchasePrice);
			res.appendChild(quantity);

			if (callback) callback(item, product, res);
		}).catch(error => Status.ShowError(error));
	}
};
