import Permissions from '../../api/employee/permissions.mjs';
import Status from '../../status.mjs';


let elCode = document.getElementById('code');
let elDescription = document.getElementById('description');
let elSystem = document.getElementById('system');
let elStatus = document.getElementById('status');
let elCreatedAt = document.getElementById('created_at');
let elAction = document.getElementById('action');

const pathName = window.location.pathname;
const sepPos = pathName.lastIndexOf('/');
if (sepPos != -1) {
	const permissionId = parseInt(pathName.substring(sepPos + 1));
	console.log(permissionId);
	Permissions.Get(permissionId).then(r => {
		elCode.innerHTML = `Код: ${r['permission']['code']}`;
		elDescription.innerHTML = `Описание: ${r['permission']['code']}`;
		elSystem.innerHTML = 'Системное: ' + (r['permission']['is_system'] ? 'Да' : 'Нет');

		if (r['permission']['deactivated_at']) {
			elStatus.innerHTML = 'Статус: деактивировано';
			elStatus.style.color = "red";

			elAction.classList.add('green-bg');
			elAction.innerHTML = 'Активировать';
			elAction.addEventListener('click', () => {
				Permissions.Restore(permissionId).then(r => {
					window.location.href = `/employee/permission/${permissionId}`;
				}).catch(e => Status.ShowError(e));
			});
		}
		else {
			elStatus.innerHTML = 'Статус: активно';
			elStatus.style.color = "lime";

			elAction.classList.add('orange-bg');
			elAction.innerHTML = 'Деактивировать';
			elAction.addEventListener('click', () => {
				Permissions.Deactivate(permissionId).then(r => {
					window.location.href = `/employee/permission/${permissionId}`;
				}).catch(e => Status.ShowError(e));
			});
		}

		elCreatedAt.innerHTML = `Создано: ${new Date(r['permission']['created_at']).toISOString().slice(0, 19).replace('T', ' ')}`;
	}).catch(e => Status.ShowError(e));
}
