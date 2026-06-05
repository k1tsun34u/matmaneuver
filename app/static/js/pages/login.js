import Status from '../status.mjs';
import Auth from '../api/client/auth.mjs';


let elPhoneOrEmail = document.getElementById('phone_or_email');
let elPassword = document.getElementById('password');
let elLogin = document.getElementById('login');
let elLoginEmployee = document.getElementById('login_employee');

elLogin.addEventListener('click', e => {
	let phoneOrEmail = elPhoneOrEmail.value;

	let phone = null, email = null;
	if (phoneOrEmail.indexOf('@') !== -1) email = phoneOrEmail;
	else phone = phoneOrEmail;

	Auth.Login(phone, email, elPassword.value).then(result => {
		window.location.href = '/client';
	}).catch(error => Status.ShowError(error));
});

elLoginEmployee.addEventListener('click', e => {
	let phoneOrEmail = elPhoneOrEmail.value;

	let phone = null, email = null;
	if (phoneOrEmail.indexOf('@') !== -1) email = phoneOrEmail;
	else phone = phoneOrEmail;

	Auth.Login(phone, email, elPassword.value).then(result => {
		window.location.href = '/employee';
	}).catch(error => Status.ShowError(error));
});
