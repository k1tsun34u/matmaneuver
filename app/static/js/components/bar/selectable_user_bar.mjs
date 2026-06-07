export default class SelectableUserBar {
	constructor(fullName, phone, email, userId, onSelectCallback) {
		const fnSelect = () => {
			this._base.style.background = '#66a6ff';
			onSelectCallback(this.id);
		};

		this._id = userId;

		this._base = document.createElement('div');
		this._base.classList.add('hcont');
		this._base.addEventListener('click', () => fnSelect());

		this._elFullName = document.createElement('p');
		this._elFullName.classList.add('user-bar-full-name');
		this._elFullName.innerHTML = fullName;
		this._elFullName.style.fontWeight = 'bold';
		this._elFullName.style.cursor = 'pointer';

		this._elPhone = document.createElement('p');
		this._elPhone.classList.add('selectable-user-bar-phone');
		this._elPhone.innerHTML = phone;
		this._elPhone.style.cursor = 'pointer';

		this._elEmail = document.createElement('p');
		this._elEmail.classList.add('selectable-user-bar-email');
		this._elEmail.innerHTML = email;
		this._elEmail.style.cursor = 'pointer';

		this.appendChild(this._elFullName);
		this.appendChild(this._elPhone);
		this.appendChild(this._elEmail);
	}

	get base() {return this._base;}

	get id() {return this._id;}

	get email() {return this._elEmail.innerHTML;}
	set email(email) {this._elEmail.innerHTML = email ? email : 'Почта не привязана';}
	
	childNodes() {return this._base.childNodes;}
	appendChild(node) {this._base.appendChild(node);}
	prepend(node) {this._base.prepend(node);}

	deselect() {
		this._base.style.background = 'inherit';
	}
};
