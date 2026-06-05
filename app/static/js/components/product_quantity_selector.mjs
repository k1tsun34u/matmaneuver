import Status from '../status.mjs';
import Carts from '../api/client/carts.mjs';


export default class ProductQuantitySelector {
	static RequestBuild(product, callback) {
		ProductQuantitySelector.RequestProduct(
			product,
			(product, item) => {
				let lastQuantity = item['quantity'];

				let me = document.createElement('div');
				me.classList.add('hcont');
				me.classList.add('align-text-center');

				let qtyLbl = document.createElement('p');
				qtyLbl.innerHTML = 'Кол-во: ';
				qtyLbl.classList.add('qty');

				let qty = document.createElement('p');
				qty.innerHTML = item['quantity'];
				qty.classList.add('qty');

				let incQty = document.createElement('button');
				incQty.innerHTML = '+';
				incQty.classList.add('qty');
				incQty.addEventListener('click', e => {
					Carts.Add('ACTIVE', product['id']).then(response2 => {
						ProductQuantitySelector.RequestProduct(
							product,
							(product, item) => qty.innerHTML = item['quantity']
						);
					}).catch(error => Status.ShowError(error));
				});

				let decQty = document.createElement('button');
				decQty.innerHTML = '-';
				decQty.classList.add('qty');
				decQty.addEventListener('click', e => {
					if (lastQuantity > 1) Carts.Dec('ACTIVE', product['id']).then(response2 => {
						ProductQuantitySelector.RequestProduct(
							product,
							(product, item) => {
								qty.innerHTML = item['quantity'];
								lastQuantity = item['quantity'];
							}
						);
					}).catch(error => Status.ShowError(error));
				});

				me.appendChild(qtyLbl);
				me.appendChild(qty);
				me.appendChild(incQty);
				me.appendChild(decQty);
				callback(product, item, me);
			}
		);
	}

	static RequestProduct(product, callback) {
		Carts.GetItems('ACTIVE').then(response => {
			let items = response['items'];
			items.forEach(item => {
				if (item['product_id'] == product['id']) callback(product, item);
			});
		}).catch(error => Status.ShowError(error));
	}
};
