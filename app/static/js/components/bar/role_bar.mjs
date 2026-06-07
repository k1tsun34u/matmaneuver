export default class RoleBar {
	constructor(code, deactivated, roleId) {
		this._redirectUrl = `/employee/role/${roleId}`;
		this._redirectFunction = () => window.location.href = this._redirectUrl;

		this._base = document.createElement('div');
		this._base.classList.add('hcont');
		this._base.style.cursor = 'pointer';
		this._base.addEventListener('click', () => this._redirectFunction());

		this._elCode = document.createElement('p');
		this._elCode.classList.add('permission-bar-code');
		this._elCode.innerHTML = code;
		this._elCode.style.fontWeight = 'bold';
		this._elCode.style.cursor = 'pointer';
		this._elCode.addEventListener('click', () => this._redirectFunction());

		this._elStatus = document.createElement('p');
		this._elStatus.classList.add('permission-bar-status');
		this.deactivated = deactivated;
		this._elStatus.style.cursor = 'pointer';
		this._elStatus.addEventListener('click', () => this._redirectFunction());

		this._base.appendChild(this._elCode);
		this._base.appendChild(this._elStatus);
	}

	get base() {return this._base;}
	set redirectUrl(redirectUrl) {this._redirectUrl = redirectUrl;}

	get deactivated() {return this._elStatus.childNodes[0].innerHTML == 'Деактивирована';}
	set deactivated(isDeactivated) {
		if (isDeactivated) {
			this._elStatus.innerHTML = 'Деактивирована';
			this._elStatus.style.color = "red";
		}
		else {
			this._elStatus.innerHTML = 'Активна';
			this._elStatus.style.color = "lime";
		}
	}
	
	childNodes() {return this._base.childNodes;}
	appendChild(node) {this._base.appendChild(node);}
	prepend(node) {this._base.prepend(node);}
};
