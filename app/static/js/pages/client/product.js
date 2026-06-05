import Products from "../../api/client/products.mjs";
import ProductImages from '../../api/client/product_images.mjs';
import Status from "../../status.mjs";
import Carts from '../../api/client/carts.mjs';


let elProductImg = document.getElementById('product_img');
let elProductName = document.getElementById('product_name');
let elProductDescription = document.getElementById('product_description');
let elProductPrice = document.getElementById('product_price');
let elActions = document.getElementById('product_actions');

const pathname = window.location.pathname;
const sepPos = pathname.lastIndexOf('/');
if (sepPos != -1) {
	const productId = pathname.substring(sepPos + 1);
	Products.Get(productId).then(response => {
		let product = response['product'];

		elProductName.innerHTML = `Название: ${product['name']}`;
		elProductDescription.innerHTML = `Описание: ${product['description']}`;
		elProductPrice.innerHTML = `Цена: ${product['price']}₽/шт`;

		ProductImages.ByProduct(productId).then(result => {
			const images = result['images'];
			const storage_key = images.length > 0 ? images[0].storage_key : 'question.svg';
			const img_path = "/image/" + storage_key;
			elProductImg.src = img_path;
		}).catch(error => Status.ShowError(error));

		let elActionBtn = document.createElement('button');
		Carts.GetItems('WISHLIST', null, true).then(response2 => {
			let items = response2['items'];
			
			let found = false;
			items.forEach(item => {
				if (item['product_id'] == productId) found = true;
			});

			if (!found) {
				elActionBtn.innerHTML = 'Добавить в желаемое';
				elActionBtn.addEventListener('click', e => {
					Carts.Add('WISHLIST', productId).then(
						result2 => {window.location.href = pathname;}
					).catch(error => Status.ShowError(error));
				});
			}
			else {
				elActionBtn.innerHTML = 'Убрать из желаемого';
				elActionBtn.classList.add('red-bg');
				elActionBtn.addEventListener('click', e => {
					Carts.RemoveItem('WISHLIST', productId).then(
						result2 => {window.location.href = pathname;}
					).catch(error => Status.ShowError(error));
				});
			}

			elActions.appendChild(elActionBtn);
		}).catch(error => Status.ShowError(error));
	}).catch(error => Status.ShowError(error));
}
