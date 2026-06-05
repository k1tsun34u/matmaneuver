import Status from '../../status.mjs';
import OrderPayments from '../../api/client/order_payments.mjs';
import Pagination from '../../components/pagination.mjs';
import OrderPaymentBar from '../../components/order_payment_bar.mjs';


let elTgt = document.getElementById('tgt');
let elPrevPg = document.getElementById('prev_pg');
let elPageNumber = document.getElementById('page_number');
let elNextPg = document.getElementById('next_pg');

let pagination = new Pagination(
	() => (page) => OrderPayments.My(page),
	(page, response) => {
		elPageNumber.innerHTML = `Страница: ${page + 1}`;

		let payments = response['payments'];
		if (payments.length <= 0) elTgt.innerHTML = '<p>Пусто...</p>';
		else {
			elTgt.innerHTML = '';
			payments.forEach(payment => {OrderPaymentBar.RequestBuild(payment, (payment, res) => elTgt.appendChild(res));});
		}
	}
);

elPrevPg.addEventListener('click', e => pagination.prev());
elNextPg.addEventListener('click', e => pagination.next());
