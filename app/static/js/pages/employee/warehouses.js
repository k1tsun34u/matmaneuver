import QtyProductBar from "../../components/bar/qty_product_bar.mjs";
import Pagination from "../../components/pagination.mjs";
import Warehouses from '../../api/employee/warehouses.mjs';
import WarehouseBar from '../../components/bar/warehouse_bar.mjs';


let elSearch = document.getElementById('search');
let elSearchBtn = document.getElementById('search_btn');
let elCreate = document.getElementById('create');
let elExcludeDeleted = document.getElementById('exclude_deleted');
let elTgt = document.getElementById('tgt');
let elPrevPg = document.getElementById('prev_pg');
let elPageNumber = document.getElementById('page_number');
let elNextPg = document.getElementById('next_pg');

let pagination = new Pagination(
	() => (page) => Warehouses.Search(
		elSearch.value,
		page,
		elExcludeDeleted.checked
	),
	(page, r) => {
		if (r['warehouses'].length < 1) elTgt.innerHTML = '<p>Пусто...</p>';
		else {
			elTgt.innerHTML = '';
			r['warehouses'].forEach(wh => {
				let whBar = new WarehouseBar(
					wh['address'],
					wh['deleted_at'] != null,
					wh['id']
				);

				elTgt.appendChild(whBar.base);
			});
		}
	}
);

elCreate.addEventListener('click', () => {
	window.location.href = '/employee/create-warehouse';
});

elSearchBtn.addEventListener('click', () => pagination.select(0));
elPrevPg.addEventListener('click', e => pagination.prev());
elNextPg.addEventListener('click', e => pagination.next());
