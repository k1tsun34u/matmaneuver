import Status from '../status.mjs';
import Carts from '../api/client/carts.mjs';
import Products from '../api/client/products.mjs';
import ProductImages from '../api/client/product_images.mjs';
import ProductCategories from '../api/client/product_categories.mjs';
import ProductQuantitySelector from './product_quantity_selector.mjs';


export default class ClientProductCard {
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
				me.classList.add('client-product-card');
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
				let btnAddToCart = ClientProductCard._BuildButtonAddToCart(me, product);
				// ClientProductCard._RequestBuildQuantitySelector(me, product, (product, me) => {
				// 	btnAddToCart.remove();
				// 	console.log(product);
				// });

				callback(product, me);
			}).catch(error => Status.ShowError(error));
		}).catch(error => Status.ShowError(error));
	}

	static _BuildButtonAddToCart(me, product) {
		let btnAddToCart = document.createElement('button');
		btnAddToCart.innerHTML = 'Добавить в корзину';
		btnAddToCart.addEventListener(
			'click',
			e => {
				Carts.Add('ACTIVE', product['id']).then(result => {
					btnAddToCart.remove();
					ClientProductCard._RequestBuildQuantitySelector(me, product, undefined);
				});
			}
		);

		me.appendChild(btnAddToCart);
		return btnAddToCart;
	}

	static _RequestBuildQuantitySelector(me, product, callback) {
		ProductQuantitySelector.RequestBuild(product, (product, item, pqs) => {
			me.appendChild(pqs);

			let btnRemoveFromCart = document.createElement('button');
			btnRemoveFromCart.innerHTML = 'Убрать';
			btnRemoveFromCart.classList.add('red-bg');
			btnRemoveFromCart.addEventListener('click', e => {
				Carts.RemoveItem('ACTIVE', product['id']).then(response2 => {
					btnRemoveFromCart.remove();
					pqs.remove();
					ClientProductCard._BuildButtonAddToCart(me, product);
					if (callback) callback(product, me);
				});
			});

			me.appendChild(btnRemoveFromCart);
		});
	}
}
