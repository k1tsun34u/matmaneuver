import Warehouses from '../../api/employee/warehouses.mjs';
import Pagination from '../../components/pagination.mjs';
import Status from '../../status.mjs';


let elAddress = document.getElementById('address');
let elDescription = document.getElementById('description');
let elSetDescription = document.getElementById('set_description');
let elSupplies = document.getElementById('supplies');
let elWriteOffs = document.getElementById('write_offs');
let elTgt = document.getElementById('tgt');
let elPrevPg = document.getElementById('prev_pg');
let elPageNumber = document.getElementById('page_number');
let elNextPg = document.getElementById('next_pg');

const pathName = window.location.pathname;
const sepPos = pathName.lastIndexOf('/');
if (sepPos != -1) {
	const warehouseId = parseInt(pathName.substring(sepPos + 1));
	Warehouses.Get(warehouseId).then(r => {
		elAddress.innerHTML = `Адрес: ${r['warehouse']['address']}`;
		elDescription.value = r['warehouse']['description'];

		elSetDescription.addEventListener('click', () => {
			Warehouses.SetDescription(warehouseId, elDescription.value).then(r2 => {
				window.location.href = `/employee/warehouse/${warehouseId}`;
			}).catch(e => Status.ShowError(e));
		});

		elSupplies.href = `/employee/warehouse/${warehouseId}/supplies`
		elWriteOffs.href = `/employee/warehouse/${warehouseId}/write-offs`
	}).catch(e => Status.ShowError(e));

	let pagination = new Pagination(
		() => (page) => Warehouses.GetProductsByWarehouse(
			warehouseId,
			page
		),
		(page, r) => {
			elPageNumber.innerHTML = `Страница: ${page + 1}`;

			console.log(r);
			if (r['products'].length < 1) elTgt.innerHTML = '<p>Пусто...</p>';
			else {
				elTgt.innerHTML = '';
				r['products'].forEach(product => {
					console.log(product);
				});
			}
		}
	);

	elPrevPg.addEventListener('click', e => pagination.prev());
	elNextPg.addEventListener('click', e => pagination.next());
}
