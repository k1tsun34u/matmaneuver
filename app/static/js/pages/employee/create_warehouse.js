import Warehouses from '../../api/employee/warehouses.mjs';
import Status from '../../status.mjs';


let elAddress = document.getElementById('address');
let elDescription = document.getElementById('description');
let elCreate = document.getElementById('create');

elCreate.addEventListener('click', () => {
	Warehouses.Create(elAddress.value, elDescription.value).then(r => {
		window.location.href = '/employee/warehouses';
	}).catch(e => Status.ShowError(e));
});
