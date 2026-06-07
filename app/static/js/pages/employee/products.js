import Status from '../../status.mjs';
import Products from '../../api/employee/products.mjs';
import ProductImages from '../../api/employee/product_images.mjs';
import ProductCategories from '../../api/employee/product_categories.mjs';
import Pagination from '../../components/pagination.mjs';
import EditableCard from '../../components/card/editable_card.mjs';


let elSearch = document.getElementById('search');
let elSearchBtn = document.getElementById('search_btn');
let elMinPrice = document.getElementById('min_price');
let elMaxPrice = document.getElementById('max_price');
let elExcludeDeleted = document.getElementById('exclude_deleted');
let elTgt = document.getElementById('tgt');
let elPrevPg = document.getElementById('prev_pg');
let elPageNumber = document.getElementById('page_number');
let elNextPg = document.getElementById('next_pg');

let pagination = new Pagination(
	() => (page) => Products.Search(
		elSearch.value,
		page,
		elMinPrice.value,
		elMaxPrice.value,
		elExcludeDeleted.checked
	),
	(page, r) => {
		elPageNumber.innerHTML = `Страница: ${page + 1}`;

		let products = r['products'];
		if (products.length <= 0) elTgt.innerHTML = '<p>Пусто...</p>';
		else {
			elTgt.innerHTML = '';
			products.forEach(p => {
				let editableCard = new EditableCard(
					`/employee/product/${p['id']}`,
					null,
					p['name'],
					p['price'],
					p['id']
				);

				ProductImages.ByProduct(p['id']).then(r => {
					const images = r['images'];
					if (images.length > 0) editableCard.storageKey = images[0]['storage_key'];
				}).catch(e => Status.ShowError(e));
				elTgt.appendChild(editableCard.base);
			});
		}
	}
);

elSearchBtn.addEventListener('click', () => pagination.select(0));
elPrevPg.addEventListener('click', e => pagination.prev());
elNextPg.addEventListener('click', e => pagination.next());
