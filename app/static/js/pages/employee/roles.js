import Pagination from "../../components/pagination.mjs";
import Roles from "../../api/employee/roles.mjs";
import RoleBar from '../../components/bar/role_bar.mjs';


let elSearch = document.getElementById('search');
let elSearchBtn = document.getElementById('search_btn');
let elCreate = document.getElementById('create');
let elExcludeDeactivated = document.getElementById('exclude_deactivated');
let elTgt = document.getElementById('tgt');
let elPrevPg = document.getElementById('prev_pg');
let elPageNumber = document.getElementById('page_number');
let elNextPg = document.getElementById('next_pg');

let pagination = new Pagination(
	() => (page) => Roles.Search(
		elSearch.value,
		page,
		elExcludeDeactivated.checked
	),
	(page, r) => {
		elPageNumber.innerHTML = `Страница: ${page + 1}`;

		if (r['roles'].length < 1) elTgt.innerHTML = '<p>Пусто...</p>';
		else {
			elTgt.innerHTML = '';

			r['roles'].forEach(role => {
				let roleBar = new RoleBar(
					role['code'],
					role['deactivated_at'] != null,
					role['id']
				);

				elTgt.appendChild(roleBar.base);
			});
		}
	}
);

elCreate.addEventListener('click', () => window.location.href = '/employee/create-role');

elSearchBtn.addEventListener('click', () => pagination.select(0));
elPrevPg.addEventListener('click', e => pagination.prev());
elNextPg.addEventListener('click', e => pagination.next());
