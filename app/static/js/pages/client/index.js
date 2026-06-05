import Status from '../../status.mjs';
import Products from '../../api/employee/products.mjs';
import ProductImages from '../../api/employee/product_images.mjs';
import ProductCategories from '../../api/employee/product_categories.mjs';
import Carts from '../../api/client/carts.mjs';
import ProductQuantitySelector from '../../components/product_quantity_selector.mjs';
import ClientProductCard from '../../components/client_product_card.mjs';
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
	(page, response) => {
		elPageNumber.innerHTML = `Страница: ${page + 1}`;

		let products = response['products'];
		if (products.length <= 0) elTgt.innerHTML = '<p>Пусто...</p>';
		else {
			elTgt.innerHTML = '';
			products.forEach(p => ClientProductCard.RequestBuild(p, (product, me) => elTgt.appendChild(me)));
		}
	}
)

elSearchBtn.addEventListener('click', e => pagination.select(0));
elPrevPg.addEventListener('click', e => pagination.prev());
elNextPg.addEventListener('click', e => pagination.next());
