import Status from "../../status.mjs";
import Auth from '../../api/client/auth.mjs';
import Carts from '../../api/client/carts.mjs';
import Products from "../../api/client/products.mjs";
import ProductImages from '../../api/client/product_images.mjs';
import ProductReviews from '../../api/client/product_reviews.mjs';
import Review from "../../components/review/review.mjs";
import NewReview from "../../components/review/new_review.mjs";
import Pagination from "../../components/pagination.mjs";


let elProductImg = document.getElementById('product_img');
let elProductName = document.getElementById('product_name');
let elProductDescription = document.getElementById('product_description');
let elProductPrice = document.getElementById('product_price');
let elActions = document.getElementById('product_actions');
let elCreateReview = document.getElementById('create_review');
let elTgt = document.getElementById('tgt');
let elPrevPg = document.getElementById('prev_pg');
let elPageNumber = document.getElementById('page_number');
let elNextPg = document.getElementById('next_pg');

const pathname = window.location.pathname;
const sepPos = pathname.lastIndexOf('/');
if (sepPos != -1) {
	const productId = pathname.substring(sepPos + 1);
	Products.Get(productId).then(r => {
		elProductName.innerHTML = `Название: ${r['product']['name']}`;
		elProductDescription.innerHTML = `Описание: ${r['product']['description']}`;
		elProductPrice.innerHTML = `Цена: ${r['product']['price']} ₽/шт`;

		ProductImages.ByProduct(productId).then(result => {
			const images = result['images'];
			const storage_key = images.length > 0 ? images[0].storage_key : 'question.svg';
			const img_path = "/image/" + storage_key;
			elProductImg.src = img_path;
		}).catch(e => Status.ShowError(e));

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
						r2 => {window.location.href = pathname;}
					).catch(e => Status.ShowError(e));
				});
			}
			else {
				elActionBtn.innerHTML = 'Убрать из желаемого';
				elActionBtn.classList.add('red-bg');
				elActionBtn.addEventListener('click', e => {
					Carts.RemoveItem('WISHLIST', productId).then(
						r2 => {window.location.href = pathname;}
					).catch(e => Status.ShowError(e));
				});
			}

			elActions.appendChild(elActionBtn);
		}).catch(e => Status.ShowError(e));

		elCreateReview.addEventListener('click', () => {
			Auth.Me().then(r => {
				let newReview = new NewReview(
					r['user']['full_name'],
					(fullName, rating, comment) => {
						ProductReviews.Create(
							productId,
							rating,
							comment.length > 0 ? comment : null
						).then(r => {
							let review = new Review(fullName, rating, comment);
							elTgt.prepend(review.base);
							newReview.base.remove();
						}).catch(e => Status.ShowError(e));
					}
				);

				elTgt.prepend(newReview.base);
			}).catch(e => Status.ShowError(e));
		});
	}).catch(e => Status.ShowError(e));
	
	let pagination = new Pagination(
		() => (page) => ProductReviews.ByProduct(productId, page),
		(page, r) => {
			elPageNumber.innerHTML = `Страница: ${page + 1}`;

			if (r['reviews'].length < 1) elTgt.innerHTML = '<p>Пусто...</p>';
			else {
				elTgt.innerHTML = '';
				r['reviews'].forEach(review => {
					let elReview = new Review(review['full_name'], review['rating'], review['comment']);
					elReview.base.userId = review['user_id'];
					elReview.base.productId = review['product_id'];

					elTgt.appendChild(elReview.base);
				});

				Auth.Me().then(r => {
					for (const child of elTgt.childNodes) {
						if (child.userId == r['user']['id']) {
							if (child.lastChild.classList.contains('red-bg')) break;
							let elRemove = document.createElement('button');
							elRemove.classList.add('red-bg', 'review-remove');
							elRemove.innerHTML = 'Удалить отзыв';
							elRemove.addEventListener('click', () => {
								ProductReviews.Delete(child.productId).then(r => {
									child.remove();
								}).catch(e => Status.ShowError(e));
							});
	
							child.appendChild(elRemove);
						}
					}
				}).catch(e => Status.ShowError(e));
			}
		}
	);

	elPrevPg.addEventListener('click', e => pagination.prev());
	elNextPg.addEventListener('click', e => pagination.next());
}
