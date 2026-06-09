import WriteOffBar from '../../components/bar/write_off_bar.mjs';
import Warehouses from '../../api/employee/warehouses.mjs';
import Pagination from '../../components/pagination.mjs';
import WriteOffs from '../../api/employee/write_offs.mjs';
import DateConv from '../../date_conv.mjs';
import Status from '../../status.mjs';


let elTitle = document.getElementById('title');
let elSearch = document.getElementById('search');
let elSearchBtn = document.getElementById('search_btn');
let elCreate = document.getElementById('create');
let elSelReason = document.getElementById('sel_reason');
let elCreatedFrom = document.getElementById('created_from');
let elCreatedTo = document.getElementById('created_to');
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
		elTitle.innerHTML = `Списания со склада ${r['warehouse']['address']}`;

		let pagination = new Pagination(
			() => (page) => WriteOffs.Search(
				elSearch.value,
				page,
				warehouseId,
				elSelReason.value,
				elCreatedFrom.value,
				elCreatedTo.value
			),
			(page, r) => {
				elPageNumber.innerHTML = `Страница: ${page + 1}`;
				
				if (r['write_offs'].length < 1) elTgt.innerHTML = '<p>Пусто...</p>';
				else {
					elTgt.innerHTML = '';
					r['write_offs'].forEach(writeOff => {
						let writeOffBar = new WriteOffBar(
							writeOff['reason'],
							writeOff['created_at'],
							writeOff['id']
						);

						elTgt.appendChild(writeOffBar.base);
					});
				}
			}
		);

		elCreate.addEventListener('click', () => {
			window.location.href = `/employee/warehouse/${warehouseId}/create-write-off`;
		});
		
		elSearchBtn.addEventListener('click', () => pagination.select(0));
		elPrevPg.addEventListener('click', e => pagination.prev());
		elNextPg.addEventListener('click', e => pagination.next());
	}).catch(e => Status.ShowError(e));
}
