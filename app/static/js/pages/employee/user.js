import Users from "../../api/employee/users.mjs";
import Pagination from "../../components/pagination.mjs";
import Status from "../../status.mjs";
import ProductReviews from '../../api/employee/product_reviews.mjs';
import Review from "../../components/review/review.mjs";


let elFullName = document.getElementById('full_name');
let elPhone = document.getElementById('phone');
let elEmail = document.getElementById('email');
let elCreatedAt = document.getElementById('created_at');
let elBlockedAt = document.getElementById('blocked_at');
let elBlockedBy = document.getElementById('blocked_by');
let elDeletedAt = document.getElementById('deleted_at');
let elDeletedBy = document.getElementById('deleted_by');
let elActions = document.getElementById('actions');
let elTgt = document.getElementById('tgt');
let elPrevPg = document.getElementById('prev_pg');
let elPageNumber = document.getElementById('page_number');
let elNextPg = document.getElementById('next_pg');

const pathName = window.location.pathname;
const sepPos = pathName.lastIndexOf('/');
if (sepPos != -1) {
	let fnDateToStr = (date) => {
		if (date) return new Date(date).toISOString().slice(0, 19).replace('T', ' ');
		return 'никогда';
	}

	const userId = parseInt(pathName.substring(sepPos + 1));
	Users.Get(userId).then(r => {
		elFullName.innerHTML = `Полное имя: ${r['user']['full_name']}`;
		elPhone.innerHTML = `Номер телефона: ${r['user']['phone']}`;
		elEmail.innerHTML = `Почта: ${r['user']['email']}`;
		elCreatedAt.innerHTML = `Создан: ${fnDateToStr(r['user']['created_at'])}`;
		elBlockedAt.innerHTML = `Когда заблокирован: ${fnDateToStr(r['user']['blocked_at'])}`;
		elDeletedAt.innerHTML = `Когда удалён: ${fnDateToStr(r['user']['deleted_at'])}`;

		if (r['user']['blocked_by']) {
			elBlockedBy.innerHTML = `Кем заблокирован: ${r['user']['blocked_by_full_name']}`;

			let elUnblock = document.createElement('button');
			elUnblock.innerHTML = 'Разблокировать';
			elUnblock.addEventListener('click', () => {
				Users.Unblock(r['user']['id']).then(r2 => {
					window.location.href = `/employee/user/${r['user']['id']}`;
				}).catch(e => Status.ShowError(e));
			});

			elActions.appendChild(elUnblock);
		}
		else {
			elBlockedBy.innerHTML = 'Кем заблокирован: никем';

			let elBlock = document.createElement('button');
			elBlock.classList.add('orange-bg');
			elBlock.innerHTML = 'Заблокировать';
			elBlock.addEventListener('click', () => {
				Users.Block(r['user']['id']).then(r2 => {
					window.location.href = `/employee/user/${r['user']['id']}`;
				}).catch(e => Status.ShowError(e));
			});

			elActions.appendChild(elBlock);
		}

		if (r['user']['deleted_by']) {
			elDeletedBy.innerHTML = `Кем удалён: ${r['user']['deleted_by_full_name']}`;

			let elRestore = document.createElement('button');
			elRestore.classList.add('green-bg');
			elRestore.innerHTML = 'Восстановить';
			elRestore.addEventListener('click', () => {
				Users.Restore(r['user']['id']).then(r2 => {
					window.location.href = `/employee/user/${r['user']['id']}`;
				}).catch(e => Status.ShowError(e));
			});

			elActions.appendChild(elRestore);
		}
		else {
			elDeletedBy.innerHTML = 'Кем удалён: никем';

			let elDelete = document.createElement('button');
			elDelete.classList.add('red-bg');
			elDelete.innerHTML = 'Удалить';
			elDelete.addEventListener('click', () => {
				Users.Delete(r['user']['id']).then(r2 => {
					window.location.href = `/employee/user/${r['user']['id']}`;
				}).catch(e => Status.ShowError(e));
			});

			elActions.appendChild(elDelete);
		}
	}).catch(e => Status.ShowError(e));

	let pagination = new Pagination(
		() => (page) => ProductReviews.ByUser(userId),
		(page, r) => {
			elPageNumber.innerHTML = `Страница: ${page + 1}`;
			
			if (r['reviews'].length < 1) elTgt.innerHTML = '<p>Пусто...</p>';
			else {
				elTgt.innerHTML = '';
				r['reviews'].forEach(review => {
					let elReview = new Review(
						review['full_name'],
						review['rating'],
						review['comment']
					);

					elReview.base.childNodes[0].addEventListener('click', () => {
						window.location.href = `/employee/product/${review['product_id']}`
					});

					let elRemove = document.createElement('button');
					elRemove.classList.add('review-remove', 'red-bg');
					elRemove.innerHTML = 'Удалить отзыв';
					elRemove.addEventListener('click', () => {
						ProductReviews.Delete(review['product_id'], userId).then(r => {
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
}
