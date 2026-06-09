import DateConv from '../../date_conv.mjs';
import WriteOffReason from '../../write_off_reason.mjs';


export default class WriteOffBar {
	constructor(reason, createdAtDate, writeOffId) {
		this._redirectUrl = `/employee/write-off/${writeOffId}`;
		this._redirectFunction = () => {window.location.href = this._redirectUrl;};

		this._base = document.createElement('div');
		this._base.classList.add('hcont');

		this._elReason = document.createElement('p');
		this._elReason.classList.add('write-off-bar-reason');
		this._elReason.innerHTML = WriteOffReason.ValueToStr(reason);
		this._elReason.style.cursor = 'pointer';
		this._elReason.addEventListener('click', () => {this._redirectFunction();});

		this._elCreatedAt = document.createElement('p');
		this._elCreatedAt.classList.add('write-off-bar-created-at');
		this._elCreatedAt.innerHTML = DateConv.DateTimeToStr(createdAtDate);
		this._elCreatedAt.style.cursor = 'pointer';
		this._elCreatedAt.addEventListener('click', () => {this._redirectFunction();});

		this.appendChild(this._elReason);
		this.appendChild(this._elCreatedAt);
	}

	get base() {return this._base;}

	get redirectUrl() {return this._redirectUrl;}
	set redirectUrl(redirectUrl) {this._redirectUrl = redirectUrl;}
	
	childNodes() {return this._base.childNodes;}
	appendChild(node) {this._base.appendChild(node);}
	prepend(node) {this._base.prepend(node);}
};
