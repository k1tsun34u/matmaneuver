import SupplyBar from '../../components/bar/supply_bar.mjs';
import Warehouses from '../../api/employee/warehouses.mjs';
import Pagination from '../../components/pagination.mjs';
import Supplies from '../../api/employee/supplies.mjs';
import Status from '../../status.mjs';


let elTitle = document.getElementById('title');
let elSearchBtn = document.getElementById('search_btn');
let elCreate = document.getElementById('create');
let elSelStatus = document.getElementById('sel_status');
let elCreatedFrom = document.getElementById('created_from');
let elCreatedTo = document.getElementById('created_to');
let elPlannedDeliveryDateFrom = document.getElementById('planned_delivery_date_from');
let elPlannedDeliveryDateTo = document.getElementById('planned_delivery_date_to');
let elTgt = document.getElementById('tgt');
let elPrevPg = document.getElementById('prev_pg');
let elPageNumber = document.getElementById('page_number');
let elNextPg = document.getElementById('next_pg');

const pathname = window.location.pathname;
const lastSepPos = pathname.lastIndexOf('/');
const prevLastSepPos = pathname.lastIndexOf('/', lastSepPos - 1);
if (lastSepPos != -1 && prevLastSepPos != -1) {
	const warehouseId = pathname.substring(prevLastSepPos + 1, lastSepPos);
	Warehouses.Get(warehouseId).then(r => {
		elTitle.innerHTML = `Поставки на склад ${r['warehouse']['address']}`;

		let pagination = new Pagination(
			() => (page) => Supplies.Search(
				elSelStatus.value,
				page,
				elCreatedFrom.value, elCreatedTo.value,
				elPlannedDeliveryDateFrom.value, elPlannedDeliveryDateTo.value
			),
			(page, r) => {
				elPageNumber.innerHTML = `Страница: ${page + 1}`;
				
				if (r['supplies'].length < 1) elTgt.innerHTML = '<p>Пусто...</p>';
				else {
					elTgt.innerHTML = '';
					r['supplies'].forEach(supply => {
						let supplyBar = new SupplyBar(
							`/employee/supply/${supply['id']}`,
							new Date(supply['planned_delivery_date']).toISOString().split('T')[0],
							'?',
							supply['current_status']
						);

						Supplies.GetTotalPrice(supply['id']).then(r2 => {
							supplyBar.totalPrice = r2['total_price'];
						}).catch(e => Status.ShowError(e));
						elTgt.appendChild(supplyBar.base);
					});
				}
			}
		);

		elCreate.addEventListener('click', () => {
			window.location.href = `/employee/warehouse/${warehouseId}/create-supply`;
		});
		
		elSearchBtn.addEventListener('click', () => pagination.select(0));
		elPrevPg.addEventListener('click', e => pagination.prev());
		elNextPg.addEventListener('click', e => pagination.next());
	}).catch(e => Status.ShowError(e));
}
