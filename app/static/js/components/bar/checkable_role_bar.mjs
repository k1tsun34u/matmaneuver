export default class CheckableRoleBar {
	constructor(code, deactivated, roleId, onClickCallback) {
		this._base = document.createElement('div');
		this._base.classList.add('hcont');

		this._code = code;
		this._id = roleId;

		this._elCodeLbl = document.createElement('label');
		this._elCodeLbl.classList.add('cb-lbl');
		this._elCodeLbl.innerHTML = code;
		
		this._elCodeCheckBox = document.createElement('input');
		this._elCodeCheckBox.id = `cb_${roleId}`;
		this._elCodeCheckBox.type = 'checkbox';
		this._elCodeCheckBox.addEventListener('click', () => onClickCallback(this.id, this.checked));

		this._elCodeMark = document.createElement('span');
		this._elCodeMark.classList.add('cb-mark');

		this._elCodeLbl.appendChild(this._elCodeCheckBox);
		this._elCodeLbl.appendChild(this._elCodeMark);

		this._elStatus = document.createElement('p');
		this._elStatus.classList.add('role-bar-status');
		this.deactivated = deactivated;

		this._base.appendChild(this._elCodeLbl);
		this._base.appendChild(this._elStatus);
	}

	get base() {return this._base;}

	get deactivated() {return this._elStatus.innerHTML == 'Деактивирована';}
	set deactivated(deactivated) {
		if (deactivated) {
			this._elStatus.innerHTML = 'Деактивирована';
			this._elStatus.style.color = "red";
		}
		else {
			this._elStatus.innerHTML = 'Активна';
			this._elStatus.style.color = "lime";
		}
	}

	get checked() {return this._elCodeCheckBox.checked;}
	set checked(checked) {this._elCodeCheckBox.checked = checked;}

	get code() {return this._code;}
	get id() {return this._id;}
	
	childNodes() {return this._base.childNodes;}
	appendChild(node) {this._base.appendChild(node);}
	prepend(node) {this._base.prepend(node);}
};
