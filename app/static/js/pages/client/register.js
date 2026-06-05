import Status from '../../status.mjs';
import Auth from '../../api/client/auth.mjs';


let elFullName = document.getElementById('full_name');
let elPhone = document.getElementById('phone');
let elEmail = document.getElementById('email');
let elPassword = document.getElementById('password');
let elRegister = document.getElementById('register');
let elLogin = document.getElementById('login');

elRegister.addEventListener('click', e => {
	Auth.Register(elPhone.value, elEmail.value, elFullName.value, elPassword.value).then(result => {
		window.location.href = '/client/profile';
	}).catch(error => Status.ShowError(error));
});
