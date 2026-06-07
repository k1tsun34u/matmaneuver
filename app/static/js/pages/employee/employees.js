import Employees from '../../api/employee/employees.mjs';
import EmployeeBar from '../../components/bar/employee_bar.mjs';
import Pagination from '../../components/pagination.mjs';


let elSearch = document.getElementById('search');
let elSearchBtn = document.getElementById('search_btn');
let elCreate = document.getElementById('create');
let elExcludeFired = document.getElementById('exclude_fired');
let elTgt = document.getElementById('tgt');
let elPrevPg = document.getElementById('prev_pg');
let elPageNumber = document.getElementById('page_number');
let elNextPg = document.getElementById('next_pg');

let pagination = new Pagination(
	() => (page) => Employees.Search(
		elSearch.value,
		page,
		elExcludeFired.checked
	),
	(page, r) => {
		elPageNumber.innerHTML = `Страница: ${page + 1}`;

		if (r['employee_users'].length < 1) elTgt.innerHTML = '<p>Пусто...</p>';
		else {
			elTgt.innerHTML = '';
			r['employee_users'].forEach(eu => {
				let employeeBar = new EmployeeBar(
					eu['full_name'],
					eu['phone'],
					eu['email'],
					eu['fired_at'] != null,
					eu['id']
				);

				elTgt.appendChild(employeeBar.base);
			});
		}
	}
);

elCreate.addEventListener('click', () => {
	window.location.href = '/employee/create-employee';
});

elSearchBtn.addEventListener('click', () => pagination.select(0));
elPrevPg.addEventListener('click', e => pagination.prev());
elNextPg.addEventListener('click', e => pagination.next());
