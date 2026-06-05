import Status from '../../status.mjs';
import Carts from '../../api/client/carts.mjs';
import Pagination from '../../components/pagination.mjs';
import Products from '../../api/client/products.mjs';
import WishlistItemCard from '../../components/wishlist_item_card.mjs';


let elTgt = document.getElementById('tgt');
let elPrevPg = document.getElementById('prev_pg');
let elPageNumber = document.getElementById('page_number');
let elNextPg = document.getElementById('next_pg');

let pagination = new Pagination(
	() => (page) => Carts.GetItems('WISHLIST', page, false),
	(page, response) => {
		elPageNumber.innerHTML = `Страница: ${page + 1}`;

		let items = response['items'];
		if (items.length <= 0) elTgt.innerHTML = '<p>Пусто...</p>';
		else {
			elTgt.innerHTML = '';
			items.forEach(item => {
				WishlistItemCard.RequestBuild(item['product_id'], (product, me) => {elTgt.appendChild(me);});
			});
		}
	}
);

elPrevPg.addEventListener('click', e => pagination.prev());
elNextPg.addEventListener('click', e => pagination.next());
