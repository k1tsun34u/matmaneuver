import Pagination from "../../components/pagination.mjs";
import Suppliers from '../../api/employee/suppliers.mjs';
import SupplierBar from '../../components/bar/supplier_bar.mjs';


let elSearch = document.getElementById('search');
let elSearchBtn = document.getElementById('search_btn');
let elCreate = document.getElementById('create');
let elExcludeDeactivated = document.getElementById('exclude_deactivated');
let elTgt = document.getElementById('tgt');
let elPrevPg = document.getElementById('prev_pg');
let elPageNumber = document.getElementById('page_number');
let elNextPg = document.getElementById('next_pg');

let pagination = new Pagination(
	() => (page) => Suppliers.Search(elSearch.value, page),
	(page, r) => {
		elPageNumber.innerHTML = `Страница: ${page + 1}`;

		if (r['suppliers'].length < 1) elTgt.innerHTML = '<p>Пусто...</p>';
		else {
			elTgt.innerHTML = '';

			r['suppliers'].forEach(supplier => {
				let supplierBar = new SupplierBar(
					supplier['full_name'],
					supplier['phone'],
					supplier['deactivated_at'] != null,
					supplier['id']
				);

				elTgt.appendChild(supplierBar.base);
			});
		}
	}
);

elCreate.addEventListener('click', () => {
	window.location.href = `/employee/create-supplier`;
});

elSearchBtn.addEventListener('click', () => pagination.select(0));
elPrevPg.addEventListener('click', e => pagination.prev());
elNextPg.addEventListener('click', e => pagination.next());
