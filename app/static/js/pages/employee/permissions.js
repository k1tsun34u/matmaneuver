import Pagination from "../../components/pagination.mjs";
import Permissions from "../../api/employee/permissions.mjs";
import PermissionBar from '../../components/bar/permission_bar.mjs';


let elSearch = document.getElementById('search');
let elSearchBtn = document.getElementById('search_btn');
let elCreate = document.getElementById('create');
let elExcludeDeactivated = document.getElementById('exclude_deactivated');
let elTgt = document.getElementById('tgt');
let elPrevPg = document.getElementById('prev_pg');
let elPageNumber = document.getElementById('page_number');
let elNextPg = document.getElementById('next_pg');

let pagination = new Pagination(
	() => (page) => Permissions.Search(
		elSearch.value,
		page,
		elExcludeDeactivated.checked
	),
	(page, r) => {
		elPageNumber.innerHTML = `Страница: ${page + 1}`;

		if (r['permissions'].length < 1) elTgt.innerHTML = '<p>Пусто...</p>';
		else {
			elTgt.innerHTML = '';

			r['permissions'].forEach(permission => {
				let permissionBar = new PermissionBar(
					permission['code'],
					permission['deactivated_at'] != null,
					permission['id']
				);

				elTgt.appendChild(permissionBar.base);
			});
		}
	}
);

elCreate.addEventListener('click', () => window.location.href = '/employee/create-permission');

elSearchBtn.addEventListener('click', () => pagination.select(0));
elPrevPg.addEventListener('click', e => pagination.prev());
elNextPg.addEventListener('click', e => pagination.next());
