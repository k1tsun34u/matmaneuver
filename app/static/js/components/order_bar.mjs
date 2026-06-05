import Orders from '../api/client/orders.mjs';
import OrderStatus from '../order_status.mjs';
import Status from '../status.mjs';


export default class OrderBar {
	static Build(order, callback) {
		Orders.GetTotalPrice(order['id']).then(result => {
			const orderAmount = result['total_price'];
			const lastStatus = OrderStatus.ValueToStr(order['current_status']);
			const fnRedirect = (e) => {window.location.href = `/client/order/${order['id']}`};

			let res = document.createElement('div');
			res.classList.add('hcont');

			let trackNum = document.createElement('p');
			// let dest = document.createElement('p');
			let amount = document.createElement('p')
			let status = document.createElement('p');

			res.style.cursor = 'pointer';
			trackNum.style.cursor = 'pointer';
			// dest.style.cursor = 'pointer';
			amount.style.cursor = 'pointer';
			status.style.cursor = 'pointer';
			status.style.color = OrderStatus.StrToColor(lastStatus);

			trackNum.innerHTML = order['track_number'];
			// dest.innerHTML = order['delivery_address']
			amount.innerHTML = `${orderAmount} ₽`;
			status.innerHTML = lastStatus;

			res.addEventListener('click', e => fnRedirect(e));
			trackNum.addEventListener('click', e => fnRedirect(e));
			// dest.addEventListener('click', e => fnRedirect(e));
			amount.addEventListener('click', e => fnRedirect(e));
			status.addEventListener('click', e => fnRedirect(e));

			res.appendChild(trackNum);
			// res.appendChild(dest);
			res.appendChild(amount);
			res.appendChild(status);

			if (callback) callback(order, res);
		}).catch(error => Status.ShowError(error));
	}
};
