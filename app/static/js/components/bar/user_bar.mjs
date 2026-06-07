export default class UserBar {
	constructor(fullName, phone, email, userId) {
		this._redirectUrl = `/employee/user/${userId}`;
		this._redirectFunction = () => {window.location.href = this._redirectUrl;};

		this._base = document.createElement('div');
		this._base.classList.add('hcont');

		this._elFullName = document.createElement('p');
		this._elFullName.classList.add('user-bar-full-name');
		this._elFullName.innerHTML = fullName;
		this._elFullName.style.fontWeight = 'bold';
		this._elFullName.style.cursor = 'pointer';
		this._elFullName.addEventListener('click', () => {this._redirectFunction();});

		this._elPhone = document.createElement('p');
		this._elPhone.classList.add('order-bar-phone');
		this._elPhone.innerHTML = phone;
		this._elPhone.style.cursor = 'pointer';
		this._elPhone.addEventListener('click', () => {this._redirectFunction();});

		this._elEmail = document.createElement('p');
		this._elEmail.classList.add('order-bar-email');
		this._elEmail.innerHTML = email;
		this._elEmail.style.cursor = 'pointer';
		this._elEmail.addEventListener('click', () => {this._redirectFunction();});

		this.appendChild(this._elFullName);
		this.appendChild(this._elPhone);
		this.appendChild(this._elEmail);
	}

	get base() {return this._base;}
	set redirectUrl(redirectUrl) {this._redirectUrl = redirectUrl;}

	get email() {return this._elEmail.innerHTML;}
	set email(email) {this._elEmail.innerHTML = email ? email : 'Почта не привязана';}
	
	childNodes() {return this._base.childNodes;}
	appendChild(node) {this._base.appendChild(node);}
	prepend(node) {this._base.prepend(node);}
};
