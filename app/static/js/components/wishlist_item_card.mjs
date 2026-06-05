import ProductImages from "../api/client/product_images.mjs";
import Products from "../api/client/products.mjs";
import Status from "../status.mjs";
import Carts from '../api/client/carts.mjs';


export default class WishlistItemCard {
	static RequestBuild(productId, callback) {
		Products.Get(productId).then(response => {
			let product = response['product'];
			const fnRedirect = (e) => {window.location.href = `/client/product/${product['id']}`;}

			let res = document.createElement('div');
			res.classList.add('cart-item-bar');
			res.classList.add('hcont');

			let title = document.createElement('p');
			title.innerHTML = product['name'];
			title.addEventListener('click', e => fnRedirect(e));

			let price = document.createElement('p');
			price.innerHTML = product['price'];
			price.style.color = '#21c800';
			price.addEventListener('click', e => fnRedirect(e));

			let btnRemoveFromCart = document.createElement('button');
			btnRemoveFromCart.innerHTML = 'x';
			btnRemoveFromCart.classList.add('red-bg');
			btnRemoveFromCart.addEventListener('click', e => {
				Carts.RemoveItem('WISHLIST', productId).then(
					result => {res.remove();}
				).catch(error => Status.ShowError(error));
			});

			res.appendChild(title);
			res.appendChild(price);
			res.appendChild(btnRemoveFromCart);

			ProductImages.ByProduct(productId).then(response => {
				const images = response['images'];
				const storage_key = images.length > 0 ? images[0].storage_key : 'question.svg';
				const img_path = "/image/" + storage_key;

				let img = document.createElement('img');
				img.classList.add('cart-item-img');
				img.src = img_path;
				res.prepend(img);
			}).catch(error => Status.ShowError(error));

			if (callback) callback(product, res);
		}).catch(error => Status.ShowError(error));
	}
};