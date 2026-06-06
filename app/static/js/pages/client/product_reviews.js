import Status from '../../status.mjs';
import Auth from '../../api/client/auth.mjs';
import ProductReviews from '../../api/client/product_reviews.mjs';
import Pagination from '../../components/pagination.mjs';
import Review from '../../components/review/review.mjs';


let elTgt = document.getElementById('tgt');
let elPrevPg = document.getElementById('prev_pg');
let elPageNumber = document.getElementById('page_number');
let elNextPg = document.getElementById('next_pg');

Auth.Me().then(r => {
	const myId = r['user']['id'];
	let pagination = new Pagination(
		() => (page) => ProductReviews.ByUser(myId, page),
		(page, r) => {
			elPageNumber.innerHTML = `Страница: ${page + 1}`;

			if (r['reviews'].length < 1) elTgt.innerHTML = '<p>Пусто...</p>';
			else {
				elTgt.innerHTML = '';
				r['reviews'].forEach(review => {
					const redirectFunction = () => {window.location.href = `/client/product/${review['product_id']}`;}
					let elReview = new Review(review['name'], review['rating'], review['comment']);
					elReview.base.style.cursor = 'pointer';
					elReview.base.childNodes[0].addEventListener('click', () => {redirectFunction();});
					elReview.base.childNodes[1].addEventListener('click', () => {redirectFunction();});

					let elRemove = document.createElement('button');
					elRemove.classList.add('red-bg', 'review-remove');
					elRemove.innerHTML = 'Удалить отзыв';
					elRemove.addEventListener('click', () => {
						ProductReviews.Delete(review['product_id']).then(r => {
							elReview.base.remove();
						}).catch(e => Status.ShowError(e));
					});
					

					elReview.base.appendChild(elRemove);
					elTgt.appendChild(elReview.base);
				});
			}
		}
	);

	elPrevPg.addEventListener('click', e => pagination.prev());
	elNextPg.addEventListener('click', e => pagination.next());
}).catch(e => Status.ShowError(e));
