import Status from '../../status.mjs';
import OrderPayments from '../../api/client/order_payments.mjs';
import Pagination from '../../components/pagination.mjs';
import Orders from '../../api/client/orders.mjs';
import PaymentBar from '../../components/bar/payment_bar.mjs';
import PaymentMethod from '../../payment_method.mjs';


let elTgt = document.getElementById('tgt');
let elPrevPg = document.getElementById('prev_pg');
let elPageNumber = document.getElementById('page_number');
let elNextPg = document.getElementById('next_pg');

let pagination = new Pagination(
	() => (page) => OrderPayments.My(page),
	(page, r) => {
		elPageNumber.innerHTML = `Страница: ${page + 1}`;
		if (r['payments'].length <= 0) elTgt.innerHTML = '<p>Пусто...</p>';
		else {
			elTgt.innerHTML = '';
			r['payments'].forEach(payment => {
				let paymentBar = new PaymentBar(
					`/client/order/${payment['order_id']}`,
					'?',
					payment['amount'],
					payment['payment_method']
				);

				Orders.Get(payment['order_id']).then(
					r => {paymentBar.trackNumber = r['order']['track_number'];}
				).catch(e => Status.ShowError(e));
				elTgt.appendChild(paymentBar.base);
			});
		}
	}
);

elPrevPg.addEventListener('click', e => pagination.prev());
elNextPg.addEventListener('click', e => pagination.next());
