import Status from '../../status.mjs';
import Carts from '../../api/client/carts.mjs';
import Pagination from '../../components/pagination.mjs';
import Products from '../../api/client/products.mjs';
import ProductImages from '../../api/client/product_images.mjs'
import WishlistCard from '../../components/card/wishlist_card.mjs';


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
				Products.Get(item['product_id']).then(r => {
					let wishlistCard = new WishlistCard(
						`/client/product/${item['product_id']}`,
						null,
						r['product']['name'],
						r['product']['price'],
						item['product_id']
					);
	
					ProductImages.ByProduct(item['product_id']).then(r => {
						const images = r['images'];
						if (images.length > 0) wishlistCard.storageKey = images[0]['storage_key'];
					}).catch(e => Status.ShowError(e));
					elTgt.appendChild(wishlistCard.base);
				}).catch(e => Status.ShowError(e));
			});
		}
	}
);

elPrevPg.addEventListener('click', e => pagination.prev());
elNextPg.addEventListener('click', e => pagination.next());
