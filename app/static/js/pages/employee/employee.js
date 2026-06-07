import Employees from '../../api/employee/employees.mjs';
import Status from '../../status.mjs';
import Pagination from '../../components/pagination.mjs';
import Roles from '../../api/employee/roles.mjs';
import CheckableRoleBar from '../../components/bar/checkable_role_bar.mjs';


let elFullName = document.getElementById('full_name');
let elPhone = document.getElementById('phone');
let elEmail = document.getElementById('email');
let elCreatedAt = document.getElementById('created_at');
let elHiredAt = document.getElementById('hired_at');
let elHiredBy = document.getElementById('hired_by');
let elFiredAt = document.getElementById('fired_at');
let elFiredBy = document.getElementById('fired_by');
let elAction = document.getElementById('action');
let elSearch = document.getElementById('search');
let elSearchBtn = document.getElementById('search_btn');
let elTgt = document.getElementById('tgt');
let elSetRoles = document.getElementById('set_roles');
let elPrevPg = document.getElementById('prev_pg');
let elPageNumber = document.getElementById('page_number');
let elNextPg = document.getElementById('next_pg');

const pathName = window.location.pathname;
const sepPos = pathName.lastIndexOf('/');
if (sepPos != -1) {
	const employeeId = parseInt(pathName.substring(sepPos + 1));
	Employees.Get(employeeId).then(r => {
		let fnDateToStr = (date) => {
			if (date) return new Date(date).toISOString().slice(0, 19).replace('T', ' ');
			return 'никогда';
		}

		elFullName.innerHTML = `Полное имя: ${r['employee_user']['full_name']}`;
		elPhone.innerHTML = `Номер телефона: ${r['employee_user']['phone']}`;
		elEmail.innerHTML = `Почта: ${r['employee_user']['email']}`;
		elCreatedAt.innerHTML = `Создан: ${fnDateToStr(r['employee_user']['created_at'])}`;
		elHiredAt.innerHTML = `Когда нанят: ${fnDateToStr(r['employee_user']['hired_at'])}`;
		elHiredBy.innerHTML = `Кем нанят: ${r['employee_user']['hired_by_full_name'] ?? 'системой'}`;
		elFiredAt.innerHTML = `Когда уволен: ${fnDateToStr(r['employee_user']['fired_at'])}`;
		elFiredBy.innerHTML = `Кем уволен: ${r['employee_user']['fired_by_full_name'] ?? 'никем'}`;

		if (r['employee_user']['fired_by_full_name']) {
			let elRehire = document.createElement('button');
			elRehire.classList.add('green-bg');
			elRehire.innerHTML = 'Нанять заново';
			elRehire.addEventListener('click', () => {
				Employees.Rehire(r['employee_user']['id']).then (r2 => {
					window.location.href = `/employee/employee/${r['employee_user']['id']}`;
				}).catch(e => Status.ShowError(e));
			});

			elAction.appendChild(elRehire);
		}
		else {
			let elFire = document.createElement('button');
			elFire.classList.add('red-bg');
			elFire.innerHTML = 'Уволить';
			elFire.addEventListener('click', () => {
				Employees.Fire(r['employee_user']['id']).then (r2 => {
					window.location.href = `/employee/employee/${r['employee_user']['id']}`;
				}).catch(e => Status.ShowError(e));
			});

			elAction.appendChild(elFire);
		}

		let toAssign = [], toUnassign = [];
		for (let i = 0; i < r['employee_user']['roles'].length; i++) {
			let er = r['employee_user']['roles'][i];
			toAssign.push(er['id']);
		}

		let pagination = new Pagination(
			() => (page) => Roles.Search(elSearch.value, page, true),
			(page, r) => {
				elPageNumber.innerHTML = `Страница: ${page + 1}`;
				
				if (r['roles'].length < 1) elTgt.innerHTML = '<p>Пусто...</p>';
				else {
					elTgt.innerHTML = '';

					r['roles'].forEach(role => {
						let checkableRoleBar = new CheckableRoleBar(
							role['code'],
							role['deactivated_at'] != null,
							role['id'],
							(id, checked) => {
								if (checked) {
									let index = toUnassign.indexOf(role['id']);
									if (index != -1) toUnassign.splice(index, 1);

									index = toAssign.indexOf(role['id']);
									if (index == -1) toAssign.push(role['id']);
								}
								else {
									let index = toAssign.indexOf(role['id']);
									if (index != -1) toAssign.splice(index, 1);

									index = toUnassign.indexOf(role['id']);
									if (index == -1) toUnassign.push(role['id']);
								}
							}
						);

						if (toAssign.indexOf(role['id']) != -1) checkableRoleBar.checked = true;
						elTgt.appendChild(checkableRoleBar.base);
					});
				}
			}
		);

		elSetRoles.addEventListener('click', () => {
			Employees.AssignRoles(employeeId, toAssign).then(r2 => {
				Employees.UnassignRoles(employeeId, toUnassign).catch(e => Status.ShowError(e));
			}).catch(e => Status.ShowError(e));
		});

		elSearchBtn.addEventListener('click', () => pagination.select(0));
		elPrevPg.addEventListener('click', e => pagination.prev());
		elNextPg.addEventListener('click', e => pagination.next());
	}).catch(e => Status.ShowError(e));
}
