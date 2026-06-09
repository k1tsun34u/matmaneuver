import Status from "../../status.mjs";
import Orders from "../../api/client/orders.mjs";
import OrderStatus from '../../order_status.mjs';
import Products from '../../api/client/products.mjs';
import ProductImages from '../../api/client/product_images.mjs';
import OrderItemBar from "../../components/bar/order_item_bar.mjs";
import DateConv from "../../date_conv.mjs";



let elOrderName = document.getElementById('order_name');
let elCreatedAt = document.getElementById('created_at');
let elStatus = document.getElementById('status');
let elAddress = document.getElementById('address');
let elAmount = document.getElementById('amount');
let elTgt = document.getElementById('tgt');

const pathname = window.location.pathname;
const sepPos = pathname.lastIndexOf('/');
if (sepPos != -1) {
	const orderId = pathname.substring(sepPos + 1);
	Orders.Get(orderId).then(response => {
		let order = response['order'];
		let status = OrderStatus.ValueToStr(order['current_status']);
		let createdAt = DateConv.DateTimeToStr(order['created_at']);

		elOrderName.innerHTML = `Заказ ${order['track_number']}`;
		elCreatedAt.innerHTML = `Создан: ${createdAt}`;
		elStatus.innerHTML = `Статус: <span style="color: ${OrderStatus.StrToColor(status)}">${status}</span>`;
		elAddress.innerHTML = `Адрес доставки: ${order['delivery_address']}`;

		let items = order['items'];
		if (items.length <= 0) elTgt.innerHTML = '<p>Пусто...</p>';
		else {
			elTgt.innerHTML = '';
			items.forEach(item => {
				let orderItemBar = new OrderItemBar(
					`/client/product/${item['product_id']}`,
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

		Orders.GetTotalPrice(orderId).then(result => {
			let amount = result['total_price'];
			elAmount.innerHTML = `Общая стоимость: <span style="color: #21c800;">${amount}₽</span>`;
			
			let elActions = document.getElementById('actions');
			if (order['current_status'] == OrderStatus.CREATED) {
				let elPayBtn = document.createElement('button');
				elPayBtn.classList.add('green-bg');
				elPayBtn.innerHTML = 'Оплатить заказ';
				elPayBtn.addEventListener('click', (e) => {
					Orders.Pay(
						orderId,
						amount			// warning: TODO: temporary solution
					).then(
						result => {window.location.href = pathname;}
					).catch(error => Status.ShowError(error));
				})

				elActions.appendChild(elPayBtn);
			}

			if (
				order['current_status'] == OrderStatus.CREATED ||
				order['current_status'] == OrderStatus.CONFIRMED
			) {
				let elCancelBtn = document.createElement('button');
				elCancelBtn.classList.add('red-bg');
				elCancelBtn.innerHTML = 'Отменить заказ';
				elCancelBtn.addEventListener('click', (e) => {
					Orders.Cancel(orderId).then(
						result => {window.location.href = pathname;}
					).catch(error => Status.ShowError(error));
				});
				
				elActions.appendChild(elCancelBtn);
			}
		}).catch(error => {
			elAmount.innerHTML = '<span class="red-bg">Общая стоимость: не удалось получить :(</span>';
			Status.ShowError(error);
		});
	}).catch(error => {
		Status.ShowError(error);
		window.location.href = '/login';
	});
}
