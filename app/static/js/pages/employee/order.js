import Status from "../../status.mjs";
import Orders from "../../api/employee/orders.mjs";
import OrderStatus from '../../order_status.mjs';
import Products from '../../api/employee/products.mjs';
import ProductImages from '../../api/employee/product_images.mjs';
import OrderItemBar from "../../components/bar/order_item_bar.mjs";
import DateConv from "../../date_conv.mjs";
import OrderPayments from '../../api/employee/order_payments.mjs';


let elOrderName = document.getElementById('order_name');
let elCreatedAt = document.getElementById('created_at');
let elAddress = document.getElementById('address');
let elFullyPaid = document.getElementById('fully_paid');
let elAmount = document.getElementById('amount');
let elSelStatus = document.getElementById('sel_status');
let elSetStatus = document.getElementById('set_status');
let elTgt = document.getElementById('tgt');

const pathname = window.location.pathname;
const sepPos = pathname.lastIndexOf('/');
if (sepPos != -1) {
	const orderId = pathname.substring(sepPos + 1);
	Orders.Get(orderId).then(r => {
		elOrderName.innerHTML = `Заказ ${r['order']['track_number']}`;
		elCreatedAt.innerHTML = `Создан: ${DateConv.DateTimeToStr(r['order']['created_at'])}`;
		elAddress.innerHTML = `Адрес доставки: ${r['order']['delivery_address']}`;
		elAmount.innerHTML = `Общая стоимость: <span style="color: #21c800;">${r['order']['total_price']}₽</span>`;
		elSelStatus.value = r['order']['current_status'];

		if (![OrderStatus.DELIVERED, OrderStatus.CANCELLED].includes(
				r['order']['current_status']
		)) elSetStatus.addEventListener('click', () => {
			Orders.SetStatus(orderId, elSelStatus.value).then(r2 => {
				window.location.href = `/employee/order/${orderId}`;
			}).catch(e => Status.ShowError(e));
		});
		else elSetStatus.remove();

		OrderPayments.IsFullyPaid(orderId).then(r2 => {
			if (r2['is_fully_paid'] == true) {
				elFullyPaid.innerHTML = `Оплачен: да`;
				elFullyPaid.style.color = '#12d400';
			}
			else {
				elFullyPaid.innerHTML = `Оплачен: нет`;
				elFullyPaid.style.color = '#cc0000';
			}
		}).catch(e => Status.ShowError(e));

		let elActions = document.getElementById('actions');
		if (r['order']['current_status'] == OrderStatus.CONFIRMED) {
			let elFulfillOrder = document.createElement('a');
			elFulfillOrder.classList.add('btn');
			elFulfillOrder.innerHTML = 'Сборка заказа...';
			elFulfillOrder.href = `/employee/order/${orderId}/fulfillment`;
			
			elActions.appendChild(elFulfillOrder);
		}

		let items = r['order']['items'];
		if (items.length <= 0) elTgt.innerHTML = '<p>Пусто...</p>';
		else {
			elTgt.innerHTML = '';
			items.forEach(item => {
				let orderItemBar = new OrderItemBar(
					`/employee/product/${item['product_id']}`,
					null,
					'?',
					item['price'],
					item['quantity']
				);

				Products.Get(item['product_id']).then(r => {
					orderItemBar.name = r['product']['name'];
				}).catch(e => Status.ShowError(e));

				ProductImages.ByProduct(item['product_id']).then(r => {
					const images = r['images'];
					if (images.length > 0) orderItemBar.storageKey = images[0]['storage_key'];
				}).catch(e => Status.ShowError(e));
				elTgt.appendChild(orderItemBar.base);
			});
		}
	}).catch(e => Status.ShowError(e));
}