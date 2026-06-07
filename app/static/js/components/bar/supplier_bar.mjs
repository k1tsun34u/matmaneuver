export default class SupplierBar {
	constructor(fullName, phone, deactivated, supplierId) {
		this._redirectUrl = `/employee/supplier/${supplierId}`;
		this._redirectFunction = () => {window.location.href = this._redirectUrl;};

		this._base = document.createElement('div');
		this._base.classList.add('hcont');

		this._elFullName = document.createElement('p');
		this._elFullName.classList.add('supplier-bar-full-name');
		this._elFullName.innerHTML = fullName;
		this._elFullName.style.fontWeight = 'bold';
		this._elFullName.style.cursor = 'pointer';
		this._elFullName.addEventListener('click', () => {this._redirectFunction();});

		this._elPhone = document.createElement('p');
		this._elPhone.classList.add('supplier-bar-phone');
		this._elPhone.innerHTML = phone;
		this._elPhone.style.cursor = 'pointer';
		this._elPhone.addEventListener('click', () => {this._redirectFunction();});

		this._elStatus = document.createElement('p');
		this._elStatus.classList.add('permission-bar-status');
		this.deactivated = deactivated;
		this._elStatus.style.cursor = 'pointer';
		this._elStatus.addEventListener('click', () => {this._redirectFunction();});

		this._base.appendChild(this._elFullName);
		this._base.appendChild(this._elPhone);
		this._base.appendChild(this._elStatus);
	}

	get base() {return this._base;}
	set redirectUrl(redirectUrl) {this._redirectUrl = redirectUrl;}

	get deactivated() {return this._elStatus.innerHTML == 'Деактивирован';}
	set deactivated(deactivated) {
		if (deactivated) {
			this._elStatus.innerHTML = 'Деактивирован';
			this._elStatus.style.color = "red";
		}
		else {
			this._elStatus.innerHTML = 'Активен';
			this._elStatus.style.color = "lime";
		}
	}
	
	childNodes() {return this._base.childNodes;}
	appendChild(node) {this._base.appendChild(node);}
	prepend(node) {this._base.prepend(node);}
};
