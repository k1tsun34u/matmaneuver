import Status from '../../status.mjs';
import Auth from '../../api/client/auth.mjs';
import ProductReviews from '../../api/client/product_reviews.mjs';


let tgt = document.getElementById('tgt');

Auth.Me().then(response => {
	let user = response['user'];

	ProductReviews.ByUser(user.id, 0).then(result => {
		const pagination = result['pagination'];
		const reviews = result['reviews'];
		reviews.forEach(i => {
			// TODO:
		});
	}).catch(error => Status.ShowError(error));
}).catch(error => Status.ShowError(error));
