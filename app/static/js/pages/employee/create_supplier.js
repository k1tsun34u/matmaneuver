import Suppliers from '../../api/employee/suppliers.mjs';
import Status from '../../status.mjs';


let elFullName = document.getElementById('full_name');
let elPhone = document.getElementById('phone');
let elEmail = document.getElementById('email');
let elAddress = document.getElementById('address');
let elCreate = document.getElementById('create');

elCreate.addEventListener('click', () => {
	Suppliers.Create(elFullName.value, elPhone.value, elEmail.value, elAddress.value).then(r => {
		window.location.href = '/employee/suppliers';
	}).catch(e => Status.ShowError(e));
});
