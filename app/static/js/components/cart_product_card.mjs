import Status from '../status.mjs';
import Carts from '../api/client/carts.mjs';
import Products from '../api/client/products.mjs';
import ProductImages from '../api/client/product_images.mjs';
import ProductCategories from '../api/client/product_categories.mjs';
import ProductQuantitySelector from './product_quantity_selector.mjs';


export default class CartProductCard {
	static RequestBuild(product, callback) {
		ProductImages.ByProduct(product['id']).then(response => {
			const images = response['images'];
			const storage_key = images.length > 0 ? images[0].storage_key : 'question.svg';
			const img_path = "/image/" + storage_key;
			ProductCategories.ByProduct(product['id']).then(result => {
				const fnRedirect = (e) => {
					window.location.href = `/client/product/${product['id']}`;
				}
	
				let me = document.createElement('div');
				me.classList.add('cart-product-card');
				me.classList.add('vcont');
				
				let img = document.createElement('img');
				img.classList.add('product-image');
				img.src = img_path;
				img.addEventListener('click', e => fnRedirect(e));
	
				let title = document.createElement('p');
				title.innerHTML = product['name'];
				title.addEventListener('click', e => fnRedirect(e));
	
				let price = document.createElement('p');
				price.innerHTML = product['price'];
				price.style.color = '#21c800';
				price.addEventListener('click', e => fnRedirect(e));

				me.appendChild(img);
				me.appendChild(title);
				me.appendChild(price);
				ProductQuantitySelector.RequestBuild(product, (product, item, pqs) => {
					me.appendChild(pqs);

					let btnRemoveFromCart = document.createElement('button');
					btnRemoveFromCart.innerHTML = 'Убрать';
					btnRemoveFromCart.classList.add('red-bg');
					btnRemoveFromCart.addEventListener('click', e => {
						Carts.RemoveItem('ACTIVE', product['id']).then(response2 => me.remove());
					});

					me.appendChild(btnRemoveFromCart);
				});

				if (callback) callback(product, me);
			}).catch(error => Status.ShowError(error));
		}).catch(error => Status.ShowError(error));
	}
}
