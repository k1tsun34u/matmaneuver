import Status from '../../status.mjs';
import Products from '../../api/client/products.mjs';
import ProductImages from '../../api/client/product_images.mjs';
import ProductCategories from '../../api/client/product_categories.mjs';
import Carts from '../../api/client/carts.mjs';
import ProductCard from '../../components/card/product_card.mjs';
import Pagination from '../../components/pagination.mjs';


let elSearch = document.getElementById('search');
let elSearchBtn = document.getElementById('search_btn');
let elMinPrice = document.getElementById('min_price');
let elMaxPrice = document.getElementById('max_price');
let elTgt = document.getElementById('tgt');
let elPrevPg = document.getElementById('prev_pg');
let elPageNumber = document.getElementById('page_number');
let elNextPg = document.getElementById('next_pg');

let pagination = new Pagination(
	() => (page) => Products.Search(
		elSearch.value,
		page,
		elMinPrice.value,
		elMaxPrice.value
	),
	(page, r) => {
		elPageNumber.innerHTML = `Страница: ${page + 1}`;

		let products = r['products'];
		if (products.length <= 0) elTgt.innerHTML = '<p>Пусто...</p>';
		else {
			elTgt.innerHTML = '';
			products.forEach(p => {
				let productCard = new ProductCard(
					`/client/product/${p['id']}`,
					null,
					p['name'],
					p['price'],
					p['id']
				);

				ProductImages.ByProduct(p['id']).then(r => {
					const images = r['images'];
					if (images.length > 0) productCard.storageKey = images[0]['storage_key'];
				}).catch(e => Status.ShowError(e));
				elTgt.appendChild(productCard.base);
			});
		}
	}
);

elSearchBtn.addEventListener('click', e => pagination.select(0));
elPrevPg.addEventListener('click', e => pagination.prev());
elNextPg.addEventListener('click', e => pagination.next());
