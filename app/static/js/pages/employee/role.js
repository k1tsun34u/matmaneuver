import Status from "../../status.mjs";
import Roles from "../../api/employee/roles.mjs";
import Pagination from '../../components/pagination.mjs';
import Permissions from '../../api/employee/permissions.mjs';
import CheckablePermissionBar from "../../components/bar/checkable_permission_bar.mjs";
import DateConv from "../../date_conv.mjs";


let elCode = document.getElementById('code');
let elSystem = document.getElementById('system');
let elCreatedAt = document.getElementById('created_at');
let elStatus = document.getElementById('status');
let elAction = document.getElementById('action');
let elSearch = document.getElementById('search');
let elSearchBtn = document.getElementById('search_btn');
let elTgt = document.getElementById('tgt');
let elSetPermissions = document.getElementById('set_permissions');
let elPrevPg = document.getElementById('prev_pg');
let elPageNumber = document.getElementById('page_number');
let elNextPg = document.getElementById('next_pg');

const pathName = window.location.pathname;
const sepPos = pathName.lastIndexOf('/');
if (sepPos != -1) {
	const roleId = parseInt(pathName.substring(sepPos + 1));
	Roles.Get(roleId).then(r => {
		elCode.innerHTML = `Код: ${r['role']['code']}`;
		elSystem.innerHTML = 'Системное: ' + (r['role']['is_system'] ? 'Да' : 'Нет');

		if (r['role']['deactivated_at']) {
			elStatus.innerHTML = `Статус: деактивирована`;
			elStatus.style.color = "red";
			
			elAction.classList.add('green-bg');
			elAction.innerHTML = 'Активировать';
			elAction.addEventListener('click', () => {
				Roles.Restore(roleId).then(r => {
					window.location.href = `/employee/role/${roleId}`;
				}).catch(e => Status.ShowError(e));
			});
		}
		else {
			elStatus.innerHTML = `Статус: активна`;
			elStatus.style.color = "lime";
			
			elAction.classList.add('orange-bg');
			elAction.innerHTML = 'Деактивировать';
			elAction.addEventListener('click', () => {
				Roles.Deactivate(roleId).then(r => {
					window.location.href = `/employee/role/${roleId}`;
				}).catch(e => Status.ShowError(e));
			});
		}

		elCreatedAt.innerHTML = `Создана: ${DateConv.DateTimeToStr(r['role']['created_at'])}`;

		let toAssign = [], toUnassign = [];
		for (let i = 0; i < r['role']['permissions'].length; i++) {
			let p = r['role']['permissions'][i];
			toAssign.push(p['id']);
		}

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
									let index = toUnassign.indexOf(permission['id']);
									if (index != -1) toUnassign.splice(index, 1);

									index = toAssign.indexOf(permission['id']);
									if (index == -1) toAssign.push(permission['id']);
								}
								else {
									let index = toAssign.indexOf(permission['id']);
									if (index != -1) toAssign.splice(index, 1);

									index = toUnassign.indexOf(permission['id']);
									if (index == -1) toUnassign.push(permission['id']);
								}
							}
						);

						if (toAssign.indexOf(permission['id']) != -1) checkablePermissionBar.checked = true;
						elTgt.appendChild(checkablePermissionBar.base);
					});
				}
			}
		);

		elSetPermissions.addEventListener('click', () => {
			Roles.AssignPermissions(r['role']['id'], toAssign).then(r2 => {
				Roles.UnassignPermissions(r['role']['id'], toUnassign).catch(e => Status.ShowError(e));
			}).catch(e => Status.ShowError(e));
		});

		elSearchBtn.addEventListener('click', () => pagination.select(0));
		elPrevPg.addEventListener('click', e => pagination.prev());
		elNextPg.addEventListener('click', e => pagination.next());
	}).catch(e => Status.ShowError(e));
}
