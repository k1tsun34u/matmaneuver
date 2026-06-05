import Status from '../../status.mjs';
import Products from '../../api/employee/products.mjs';
import ProductImages from '../../api/employee/product_images.mjs';
import ProductCategories from '../../api/employee/product_categories.mjs';


let total_pages = null;

function buildProductCard(el, product) {
	ProductImages.ByProduct(product['id']).then(response => {
		const images = response['images'];
		const storage_key = images.length > 0 ? images[0].storage_key : 'question.svg';
		const img_path = "/image/" + storage_key;
		ProductCategories.ByProduct(product['id']).then(result => {
			const fnRedirect = (e) => {
				window.location.href = `/client/product/${product['id']}`;
			}

			let res = document.createElement('div');
			res.classList.add('complete-product-card');
			res.classList.add('vcont');
			
			let img = document.createElement('img');
			img.classList.add('product-image');
			img.src = img_path;
			img.addEventListener('click', e => fnRedirect(e));

			let title = document.createElement('p');
			title.innerHTML = product['name'];
			title.addEventListener('click', e => fnRedirect(e));

			let price = document.createElement('p');
			price.innerHTML = product['price'];
			price.addEventListener('click', e => fnRedirect(e));

			let btnEdit = document.createElement('button');
			btnEdit.innerHTML = 'Редактировать';
			btnEdit.addEventListener('click', e => {window.location.href = `/employee/product/${product['id']}`});

			res.appendChild(img);
			res.appendChild(title);
			res.appendChild(price);
			res.appendChild(btnEdit);

			el.appendChild(res);
		}).catch(error => Status.ShowError(error));
	}).catch(error => Status.ShowError(error));
}

function selectProductsFromPage(page, search, minPrice, maxPrice, excludeDeleted) {
	Products.Search(search, page, minPrice, maxPrice, excludeDeleted).then(response => {
		let pagination = response['pagination'];
		total_pages = pagination['total_pages'];

		let products = response['products'];
		if (products.length <= 0) elTgt.innerHTML = '<p>Пусто...</p>';
		else {
			elTgt.innerHTML = '';
			products.forEach(p => buildProductCard(elTgt, p));
		}
	}).catch(error => Status.ShowError(error));
}


let elSearch = document.getElementById('search');
let elSearchBtn = document.getElementById('search_btn');
let elMinPrice = document.getElementById('min_price');
let elMaxPrice = document.getElementById('max_price');
let elExcludeDeleted = document.getElementById('exclude_deleted');
let elTgt = document.getElementById('tgt');
let elPrevPg = document.getElementById('prev_pg');
let elNextPg = document.getElementById('next_pg');

let page = 0;
selectProductsFromPage(0, elSearch.value, elMinPrice.value, elMaxPrice.value, elExcludeDeleted.checked);
elSearchBtn.addEventListener('click', e => {
	page = 0;
	selectProductsFromPage(
		page,
		elSearch.value,
		elMinPrice.value, elMaxPrice.value,
		elExcludeDeleted.checked
	);
});

elNextPg.addEventListener('click', e => {
	if (page > 0) {
		page -= 1;
		selectProductsFromPage(
			page,
			elSearch.value,
			elMinPrice.value, elMaxPrice.value,
			elExcludeDeleted.checked
		);
	}
});

elNextPg.addEventListener('click', e => {
	if (page < total_pages - 1) {
		page += 1;
		selectProductsFromPage(
			page,
			elSearch.value,
			elMinPrice.value, elMaxPrice.value,
			elExcludeDeleted.checked
		);
	}
});