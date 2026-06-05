import Status from '../../status.mjs';
import Orders from '../../api/client/orders.mjs';
import OrderBar from '../../components/order_bar.mjs';
import Pagination from '../../components/pagination.mjs';


let elSearch = document.getElementById('search');
let elSearchBtn = document.getElementById('search_btn');
let elSelStatus = document.getElementById('sel_status');
let elCreatedFrom = document.getElementById('created_from');
let elCreatedTo = document.getElementById('created_to');
let elTgt = document.getElementById('tgt');
let elPrevPg = document.getElementById('prev_pg');
let elPageNumber = document.getElementById('page_number');
let elNextPg = document.getElementById('next_pg');

let pagination = new Pagination(
	() => (page) => Orders.Search(
		elSearch.value,
		page,
		elSelStatus.value,
		elCreatedFrom.value, 
		elCreatedTo.value
	),
	(page, response) => {
		elPageNumber.innerHTML = `Страница: ${page + 1}`;

		let orders = response['orders'];
		if (orders.length <= 0) elTgt.innerHTML = '<p>Пусто...</p>';
		else {
			elTgt.innerHTML = '';
			orders.forEach(order => {OrderBar.Build(order, (order, me) => {elTgt.appendChild(me)});});
		}
	}
);

elSearchBtn.addEventListener('click', e => pagination.select(0));
elPrevPg.addEventListener('click', e => pagination.prev());
elNextPg.addEventListener('click', e => pagination.next());
