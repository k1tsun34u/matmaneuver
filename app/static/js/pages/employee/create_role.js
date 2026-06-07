import Status from "../../status.mjs";
import Roles from "../../api/employee/roles.mjs";
import Pagination from '../../components/pagination.mjs';
import Permissions from '../../api/employee/permissions.mjs';
import CheckablePermissionBar from "../../components/bar/checkable_permission_bar.mjs";


let elSearch = document.getElementById('search');
let elSearchBtn = document.getElementById('search_btn');
let elExcludeDeactivated = document.getElementById('exclude_deactivated');
let elCode = document.getElementById('code');
let elTgt = document.getElementById('tgt');
let elCreate = document.getElementById('create');
let elPrevPg = document.getElementById('prev_pg');
let elPageNumber = document.getElementById('page_number');
let elNextPg = document.getElementById('next_pg');

let toAssign = [];
let pagination = new Pagination(
	() => (page) => Permissions.Search(elSearch.value, page, true),
	(page, r) => {
		elPageNumber.innerHTML = `Страница: ${page + 1}`;

		if (r['permissions'].length < 1) elTgt.innerHTML = '<p>Пусто...</p>';
		else {
			elTgt.innerHTML = '';

			r['permissions'].forEach(permission => {
				let checkablePermissionBar = new CheckablePermissionBar(
					permission['code'],
					permission['deactivated_at'] != null,
					permission['id'],
					(id, checked) => {
						if (checked) {
							let index = toAssign.indexOf(permission['id']);
							if (index == -1) toAssign.push(permission['id']);
						}
						else {
							let index = toAssign.indexOf(permission['id']);
							if (index != -1) toAssign.splice(index, 1);
						}
					}
				);

				if (toAssign.indexOf(permission['id']) != -1) checkablePermissionBar.checked = true;
				elTgt.appendChild(checkablePermissionBar.base);
			});
		}
	}
);

elCreate.addEventListener('click', () => {
	Roles.Create(elCode.value, false).then(r => {
		Roles.AssignPermissions(r['role_id'], toAssign).then(r => {
			window.location.href = '/employee/roles';
		}).catch(e => Status.ShowError(e));
	}).catch(e => Status.ShowError(e));
});

elSearchBtn.addEventListener('click', () => pagination.select(0));
elPrevPg.addEventListener('click', e => pagination.prev());
elNextPg.addEventListener('click', e => pagination.next());
