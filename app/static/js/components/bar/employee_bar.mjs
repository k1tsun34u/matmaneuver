export default class EmployeeBar {
	constructor(fullName, phone, email, fired, employeeId) {
		this._redirectUrl = `/employee/employee/${employeeId}`;
		this._redirectFunction = () => {window.location.href = this._redirectUrl;};

		this._base = document.createElement('div');
		this._base.classList.add('hcont');

		this._elFullName = document.createElement('p');
		this._elFullName.classList.add('employee-bar-full-name');
		this._elFullName.innerHTML = fullName;
		this._elFullName.style.fontWeight = 'bold';
		this._elFullName.style.cursor = 'pointer';
		this._elFullName.addEventListener('click', () => {this._redirectFunction();});

		this._elPhone = document.createElement('p');
		this._elPhone.classList.add('employee-bar-phone');
		this._elPhone.innerHTML = phone;
		this._elPhone.style.cursor = 'pointer';
		this._elPhone.addEventListener('click', () => {this._redirectFunction();});

		this._elEmail = document.createElement('p');
		this._elEmail.classList.add('employee-bar-email');
		this._elEmail.innerHTML = email;
		this._elEmail.style.cursor = 'pointer';
		this._elEmail.addEventListener('click', () => {this._redirectFunction();});

		this._elFired = document.createElement('p');
		this._elFired.classList.add('employee-bar-email');
		this.fired = fired;
		this._elFired.style.cursor = 'pointer';
		this._elFired.addEventListener('click', () => {this._redirectFunction();});

		this.appendChild(this._elFullName);
		this.appendChild(this._elPhone);
		this.appendChild(this._elEmail);
		this.appendChild(this._elFired);
	}

	get base() {return this._base;}
	set redirectUrl(redirectUrl) {this._redirectUrl = redirectUrl;}

	get email() {return this._elEmail.innerHTML;}
	set email(email) {this._elEmail.innerHTML = email ? email : 'Почта не привязана';}

	get fired() {return this._elFired.innerHTML == 'Уволен';}
	set fired(fired) {
		if (fired) {
			this._elFired.innerHTML = 'Уволен';
			this._elFired.style.color = "red";
		}
		else {
			this._elFired.innerHTML = 'Работает';
			this._elFired.style.color = "lime";
		}
	}
	
	childNodes() {return this._base.childNodes;}
	appendChild(node) {this._base.appendChild(node);}
	prepend(node) {this._base.prepend(node);}
};
