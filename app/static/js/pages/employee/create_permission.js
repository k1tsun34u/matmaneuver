import Permissions from "../../api/employee/permissions.mjs";
import Status from "../../status.mjs";


let elCode = document.getElementById('code');
let elDescription = document.getElementById('description');
let elCreate = document.getElementById('create');

elCreate.addEventListener('click', () => {
	Permissions.Create(elCode.value, elDescription.value, false).then(r => {
		window.location.href = '/employee/permissions';
	}).catch(e => Status.ShowError(e));
});
