import Status from '../status.mjs';
import Orders from '../api/client/orders.mjs';
import PaymentMethod from '../payment_method.mjs';


export default class OrderPaymentBar {
	static RequestBuild(payment, callback) {
		let createdAt = new Date(payment['created_at']).toISOString().slice(0, 19).replace('T', ' ');
		let fnRedirect = (e) => {window.location.href = `/client/order/${payment['order_id']}`;}

		let res = document.createElement('div');
		res.classList.add('hcont');
		res.style.cursor = 'pointer';
		res.addEventListener('click', fnRedirect);

		let number = document.createElement('p');
		let trackNum = document.createElement('p');
		trackNum.classList.add('order-payment-track-num');

		let date = document.createElement('p');
		let amount = document.createElement('p');
		let method = document.createElement('p');

		number.innerHTML = `#${payment['id']}`;
		trackNum.innerHTML = `?`;
		date.innerHTML = createdAt;
		amount.innerHTML = `${payment['amount']}₽`;
		method.innerHTML = PaymentMethod.ValueToStr(payment['payment_method']);

		number.style.maxWidth = '7%';
		number.style.cursor = 'pointer';
		trackNum.style.cursor = 'pointer';
		date.style.cursor = 'pointer';
		amount.style.color = '#21c800';
		amount.style.cursor = 'pointer';
		method.style.color = PaymentMethod.StrToColor(method.innerHTML);
		method.style.cursor = 'pointer';

		number.addEventListener('click', fnRedirect);
		trackNum.addEventListener('click', fnRedirect);
		date.addEventListener('click', fnRedirect);
		amount.addEventListener('click', fnRedirect);
		method.addEventListener('click', fnRedirect);

		res.appendChild(number);
		res.appendChild(trackNum);
		res.appendChild(date);
		res.appendChild(amount);
		res.appendChild(method);

		Orders.Get(payment['order_id']).then(result => {
			let order = result['order']

			trackNum.innerHTML = order['track_number'];
			if (callback) callback(payment, res);
		}).catch(error => {
			Status.ShowError(error);
			if (callback) callback(payment, res);
		});
	}
};
