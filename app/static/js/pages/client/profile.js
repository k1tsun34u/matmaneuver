import Status from '../../status.mjs';
import Auth from '../../api/client/auth.mjs';
import Cookies from '../../cookies.mjs';


let elFullName = document.getElementById('full_name');
let elPhone = document.getElementById('phone');
let elEmail = document.getElementById('email');
let elPassword = document.getElementById('password');
let elUpdate = document.getElementById('update');
let elSetPassword = document.getElementById('set_password');
let elLogOut = document.getElementById('logout');

Auth.Me().then(result => {
	let user = result['user'];
	elFullName.value = user['full_name'];
	elPhone.value = user['phone'];
	elEmail.value = user['email'];
	elPassword.value = '';
}).catch(error => {
	Status.ShowError(error);
	window.location.href = '/login';
});

elUpdate.addEventListener('click', e => {
	Auth.Update(
		elPhone.value ? elPhone.value : "__NONE__",
		elEmail.value ? elEmail.value : "__NONE__",
		elFullName.value ? elFullName.value : "__NONE__"
	).then(result => {
		window.location.href = '/client/profile';
	}).catch(error => Status.ShowError(error));
});

elSetPassword.addEventListener('click', e => {
	Auth.SetPassword(elPassword.value ? elPassword.value : "__NONE__").then(result => {
		window.location.href = '/login';
	}).catch(error => Status.ShowError(error));
});

elLogOut.addEventListener('click', e => {
	Cookies.Set('session', undefined);
	window.location.href = '/login';
});